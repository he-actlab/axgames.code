package Sobel;

import java.io.IOException;
import java.util.Random;
import java.util.StringTokenizer;

import Sobel.TextFile.Mode;


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

	public void load() throws IOException {
		TextFile textFile = new TextFile (inputFilePath, Mode.READ);

		width = textFile.loadInt();
		textFile.loadChar();
		height = textFile.loadInt();

		image = new int[height][][];
		for (int i=0; i<height; i++){
			image[i] = new int[width][];
			for(int j=0; j<width; j++){
				image[i][j] = new int[3];
			}
		}

		for (int i = 0; i < height; ++i) {
			for (int j = 0; j < width; j++) {
				image[i][j][0] = textFile.loadInt();
				textFile.loadChar();
				image[i][j][1] = textFile.loadInt();
				textFile.loadChar();
				image[i][j][2] = textFile.loadInt();
				if (j < (width - 1)) {
					textFile.loadChar();
				}
			}
		}
	}
	
	public void initOutputImage() {
		outputImage = new int[height][][];
		for (int i=0; i<height; i++){
			outputImage[i] = new int[width][];
			for(int j=0; j<width; j++){
				outputImage[i][j] = new int[3];
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

	public void saveOutput(int h, int w, int L) {
		for (int i=0; i<3; i++)
			outputImage[h][w][i] = L;
	}
	
	public void save(String suffix, int[][][] saveImage) throws IOException {
		String[] list = inputFilePath.split("/");
		StringTokenizer st = new StringTokenizer(list[list.length-1], ".");
		String newFilePath = st.nextToken() + suffix;
		
		TextFile textFile = new TextFile (outDirPath + "/" + mode + "/" + newFilePath, Mode.WRITE);
		
		textFile.save(width);
		textFile.save(",");
		textFile.save(height);
		textFile.save("\n");
		
		for (int i = 0; i < height; ++i) {
			for (int j = 0; j < width; j++) {
				textFile.save(saveImage[i][j][0]);
				textFile.save(",");
				textFile.save(saveImage[i][j][1]);
				textFile.save(",");
				textFile.save(saveImage[i][j][2]);
				if (j < (width - 1)) {
					textFile.save(",");
				}
			}
			textFile.save("\n");
		}
		textFile.close();
	}
	
	public void degradeImage(int[][][] newImage, float probApprox, float errorRate) {
		Random r = new Random();
		for (int i = 0; i < height; ++i) {
			for (int j = 0; j < width; j++) {
				float newValue;
				if (r.nextFloat() < probApprox) {
					if (r.nextFloat() < 0.5) {
						newValue = r.nextInt(255);
					} else {
						float error;
						error = outputImage[i][j][0] * errorRate;
						newValue = r.nextFloat() > 0.5 ? outputImage[i][j][0] + error : outputImage[i][j][0] - error;	
					}
					if (newValue > 255.0) newValue = 255.0f;
					if (newValue < 0.0) newValue = 0.0f;
					System.out.println("Old(" + outputImage[i][j][0] + ") New(" + newValue + ")	");
					newImage[i][j][0] = (int)newValue;
					newImage[i][j][1] = (int)newValue;
					newImage[i][j][2] = (int)newValue;
				} else {
					newValue = outputImage[i][j][0];
				}
				newImage[i][j][0] = (int)newValue;
				newImage[i][j][1] = (int)newValue;
				newImage[i][j][2] = (int)newValue;				
			}
		}
	}
	
	public void degrade () throws IOException {
		int[][][] newImage;
		newImage = new int[height][][];
		for (int i=0; i<height; i++){
			newImage[i] = new int[width][];
			for(int j=0; j<width; j++){
				newImage[i][j] = new int[3];
			}
		}
		
		// Stuff added by Akshay 
		//System.out.println("Inside Degrade function");
		int count = 0;
		boolean deg_1 = false;
		boolean deg_3 = false;
		boolean deg_5 = false;
		boolean deg_10 = false;
		boolean deg_20 = false;
		boolean deg_30 = false;
		boolean deg_50 = false;
		// Stuff added by Akshay ends
		
		for (int i = 1; i <= 1000; i++) {
			for (int j = 1; j <= 1000; j++) { 
				degradeImage (newImage, i * 0.01f, j * 0.01f);
				double nrmse = getNRMSE(outputImage, newImage);
				
				// Stuff added by Akshay
				count++;
				
				// Code to save the image for degradation 1%
				if (nrmse >= 0.01 && nrmse <= 0.011 && !deg_1) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_1 = true;
				   
				   	double psnr = getPSNR(outputImage, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				// Code to save the image for degradation 3%
				if (nrmse >= 0.03 && nrmse <= 0.031 && !deg_3) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_3 = true;
				   
				   	double psnr = getPSNR(outputImage, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				// Code to save the image for degradation 5%
				if (nrmse >= 0.05 && nrmse <= 0.051 && !deg_5) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_5 = true;
				   
				   	double psnr = getPSNR(outputImage, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				// Code to save the image for degradation 10%
				if (nrmse >= 0.10 && nrmse <= 0.101 && !deg_10) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_10 = true;
				   
				   	double psnr = getPSNR(outputImage, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				// Code to save the image for degradation 20%
				if (nrmse >= 0.20 && nrmse <= 0.201 && !deg_20) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_20 = true;
				   
				   	double psnr = getPSNR(outputImage, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				// Code to save the image for degradation 30%
				if (nrmse >= 0.30 && nrmse <= 0.301 && !deg_30) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_30 = true;
				   
				   	double psnr = getPSNR(outputImage, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				// Code to save the image for degradation 50%
				if (nrmse >= 0.50 && nrmse <= 0.501 && !deg_50) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_50 = true;
				   
				   	double psnr = getPSNR(outputImage, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				if(deg_1 && deg_3 && deg_5 && deg_10 && deg_20 && deg_30/* && deg_50*/)
					return;
				
				// Stuff added by Akshay ends
				
				
			}
		}
			
	}
	
	public double getNRMSE (int[][][] orgImage, int[][][] newImage){
		int diff;
		long sum = 0 ;
		for (int i=0; i<height; i++){
			for(int j=0; j<width; j++){
				diff = Math.abs(newImage[i][j][0] - orgImage[i][j][0]);
				sum += diff * diff;
			}
		}
		double rmse = Math.sqrt(sum / (height * width));
		double nrmse = rmse / 255.0;
		
		return nrmse;
	}
	
	public double getPSNR (int[][][] orgImage, int[][][] newImage) {
		int diff;
		long sum = 0 ;
		for (int i=0; i<height; i++){
			for(int j=0; j<width; j++){
				diff = Math.abs(newImage[i][j][0] - orgImage[i][j][0]);
				sum += diff * diff;
			}
		}
		double mse = sum / (height * width);
		double psnr = 10 * Math.log10(255.0 * 255.0 / mse); 
		
		return psnr;
	}
	
	public static void main(String[] args) throws IOException {
		RgbImage rgbImage = new RgbImage(args[0], args[1], args[2]);
		rgbImage.load();
		rgbImage.initOutputImage();
		
		rgbImage.makeGrayscale();
		
		// Stuff added by Akshay		
		System.out.println("Starting Java code");
		// Stuff added by Akshay ends

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
				rgbImage.saveOutput(y, x, L);
			}
		}
		
		rgbImage.degrade();
		rgbImage.save("-sobel.rgb", rgbImage.outputImage);
	}
}
