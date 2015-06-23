package Sobel;

import java.io.IOException;
import java.util.Arrays;
import java.util.Vector;

public class RgbImage {
	public int width;
	public int height;

	public int[][][] image;
	public int[][][] outputImage;
	
	public String inputFilePath;
	public String outDirPath;
	public String mode;
	
	public RgbImage(String inputFilePath, String outDirPath, String mode) {
		this.inputFilePath = inputFilePath;
		this.outDirPath = outDirPath;
		this.mode = mode;
	}

	public void initImage() {
		image = new int[height][][];
		for (int i=0; i<height; i++){
			image[i] = new int[width][];
			for(int j=0; j<width; j++){
				image[i][j] = new int[3];
			}
		}
		outputImage = new int[height][][];
		for (int i=0; i<height; i++){
			outputImage[i] = new int[width][];
			for(int j=0; j<width; j++){
				outputImage[i][j] = new int[3];
			}
		}
	}
	
	public void copyImage(int[][][] image) {
		for (int i=0; i<height; i++){
			for(int j=0; j<width; j++){
				for(int k=0; k<3; k++) {
					this.image[i][j][k] = image[i][j][k];
				}
			}
		}		
	}

	public void slideWindow(int x, int y, int[][][] window) {
		int h = window.length;
		int w = window[0].length;

		int x0 = x - (int)((float)w/2.);
		int x1 = x + (int)((float)w/2.);

		int y0 = y - (int)((float)h/2.);
		int y1 = y + (int)((float)h/2.);

		int r = 0;
		for (int j = y0; j <= y1; ++j) {
			if (j < 0 || j >= height) {
				for (int i = x0; i <= x1; ++i) {
					window[r][i-x0][0] = 0; 	
					window[r][i-x0][1] = 0; 	
					window[r][i-x0][2] = 0;	
				}
			} else {
				for (int i = x0; i <= x1; ++i) {
					if (i < 0 || i >= width) {
						window[r][i-x0][0] = 0; 	
						window[r][i-x0][1] = 0; 	
						window[r][i-x0][2] = 0;	
					} else {
						window[r][i-x0][0] = image[j][i][0]; 	
						window[r][i-x0][1] = image[j][i][1];	
						window[r][i-x0][2] = image[j][i][2];	
					}
				}
			}
			r++;
		}
	}

	public double sobel (int[][][] window) {
		double p1 = ( double)luminance(window[0][0]);	
		double p2 = ( double)luminance(window[0][1]);	
		double p3 = ( double)luminance(window[0][2]);	

		double p4 = ( double)luminance(window[1][0]);	
		double p5 = ( double)luminance(window[1][1]);	
		double p6 = ( double)luminance(window[1][2]);	

		double p7 = ( double)luminance(window[2][0]);	
		double p8 = ( double)luminance(window[2][1]);	
		double p9 = ( double)luminance(window[2][2]);	

		double x = (p1 + (p2 + p2) + p3 - p7 - (p8 + p8) - p9); 	
		double y = (p3 + (p6 + p6) + p9 - p1 - (p4 + p4) - p7);	

		double l = Math.sqrt(x * x + y * y);	
		
		return l;
	}

	public  int luminance(int[] rgb) {
		double rC = 0.30;	
		double gC = 0.59;	
		double bC = 0.11;	

		return (int)(rC * rgb[0] + gC * rgb[1] + bC * rgb[2] + 0.5) % 256;	
	}

	public void makeGrayscale() {
		int i;
		int j;
		double luminance;

		double rC = 0.30 / 256.0;	
		double gC = 0.59 / 256.0;	
		double bC = 0.11 / 256.0;	

		for(i = 0; i < image.length; i++) {
			for(j = 0; j < image[i].length; j++) {
				luminance = rC * image[i][j][0] + gC * image[i][j][1] + bC * image[i][j][2];	
				
				image[i][j][0] = (int)(luminance * 256);	
				image[i][j][1] = (int)(luminance * 256);	
				image[i][j][2] = (int)(luminance * 256);	
			}
		}
	}
	
	public static void main(String[] args) throws IOException {
		RgbImage rgbImage = new RgbImage(args[0], args[1], args[2]);
		
		ImageLoader imageLoader = new ImageLoader (rgbImage.mode, rgbImage.inputFilePath, rgbImage.outDirPath);
		imageLoader.load();
		
		rgbImage.width = imageLoader.getWidth();
		rgbImage.height = imageLoader.getHeight();
		
		rgbImage.initImage();
		rgbImage.copyImage(imageLoader.getImage());
		
		rgbImage.makeGrayscale();

		int[][][] window = new int[3][][];
		for(int i=0; i<3; i++){
			window[i] = new int[3][];
			for(int j=0; j<3; j++){
				window[i][j] = new int[3];
			}
		}
		
		double l;
		for (int y=0; y < rgbImage.height; y++) {
			for (int x=0; x < rgbImage.width; x++) {
				rgbImage.slideWindow(x,y, window);
				l = rgbImage.sobel(window);	
				int L = (int)(l);
				if (L >= 256)
					L = 255;
				if (L < 0)
					L = 0;
				rgbImage.outputImage[y][x][0] = L;
				rgbImage.outputImage[y][x][1] = L;
				rgbImage.outputImage[y][x][2] = L;
			}
		}
		
		ImageSaver imageSaver = new ImageSaver (rgbImage.width, rgbImage.height, rgbImage.mode, rgbImage.inputFilePath, rgbImage.outDirPath);
		imageSaver.save("-sobel.rgb", rgbImage.outputImage);
		
		Degrader degrader = new Degrader (rgbImage.width, rgbImage.height, rgbImage.outputImage, rgbImage.mode, 0.01);
		double[] errors = {0.01, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5};
		degrader.degrade(errors, imageSaver);
	}
}
