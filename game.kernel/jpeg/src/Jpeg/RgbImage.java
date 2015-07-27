package Jpeg;

import java.io.IOException;
import java.util.Arrays;
import java.util.Vector;

public class RgbImage {
	public int width;
	public int height;

	public int[][][] image;
	
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
	
	public static void main(String[] args) throws IOException {
		RgbImage rgbImage = new RgbImage(args[0], args[1], args[2]);
		
		ImageLoader imageLoader = new ImageLoader (rgbImage.mode, rgbImage.inputFilePath, rgbImage.outDirPath);
		imageLoader.load();
		
		rgbImage.width = imageLoader.getWidth();
		rgbImage.height = imageLoader.getHeight();
		
		rgbImage.initImage();
		rgbImage.copyImage(imageLoader.getImage());
		
//		rgbImage.makeGrayscale();
		
		ImageSaver imageSaver = new ImageSaver (rgbImage.width, rgbImage.height, rgbImage.mode, rgbImage.inputFilePath, rgbImage.outDirPath);
		imageSaver.save("-jpeg.rgb", rgbImage.image);
		
		TileDegrader degrader = new TileDegrader (rgbImage.width, rgbImage.height, rgbImage.image, rgbImage.mode, 0.01, rgbImage.inputFilePath);
		double[] errors = {0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 
						   0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2,
						   0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3,
						   0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4,
						   0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5};
		degrader.degrade(errors, imageSaver);
	}
}
