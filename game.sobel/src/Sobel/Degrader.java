package Sobel;

import java.io.IOException;
import java.util.Random;

public class Degrader {
	
	public int width;
	public int height;
	public int[][][] image;
	public String mode;
	
	Degrader(int width, int height, int[][][] orgImage, String mode) {
		System.out.println("width: " + width);
		this.width = width;
		this.height = height;
		initImage(orgImage);
		this.mode = mode;
	}
	
	public void initImage(int[][][] orgImage) {
		image = new int[height][][];
		for (int i=0; i<height; i++){
			image[i] = new int[width][];
			for(int j=0; j<width; j++){
				image[i][j] = new int[3];
			}
		}
		for (int i=0; i<height; i++) {
			for(int j=0; j<width; j++) {
				for (int k=0; k<3; k++) {
					image[i][j][k] = orgImage[i][j][k];
				}
			}
		}
	}
	
	private void degradeImage(int[][][] newImage, float probApprox, float errorRate) {
		Random r = new Random();
		for (int i = 0; i < height; ++i) {
			for (int j = 0; j < width; j++) {
				float newValue;
				if (r.nextFloat() < probApprox) {
					if (r.nextFloat() < 0.5) {
						newValue = r.nextInt(255);
					} else {
						float error;
						error = image[i][j][0] * errorRate;
						newValue = r.nextFloat() > 0.5 ? image[i][j][0] + error : image[i][j][0] - error;	
					}
					if (newValue > 255.0) newValue = 255.0f;
					if (newValue < 0.0) newValue = 0.0f;
//					System.out.println("Old(" + image[i][j][0] + ") New(" + newValue + ")	");
					newImage[i][j][0] = (int)newValue;
					newImage[i][j][1] = (int)newValue;
					newImage[i][j][2] = (int)newValue;
				} else {
					newValue = image[i][j][0];
				}
				newImage[i][j][0] = (int)newValue;
				newImage[i][j][1] = (int)newValue;
				newImage[i][j][2] = (int)newValue;				
			}
		}
	}
	
	public void degrade (ImageSaver imageSaver) throws IOException {
		int[][][] newImage;
		newImage = new int[height][][];
		for (int i=0; i<height; i++){
			newImage[i] = new int[width][];
			for(int j=0; j<width; j++){
				newImage[i][j] = new int[3];
			}
		}
		
		int count = 0;
		boolean deg_1 = false;
		boolean deg_3 = false;
		boolean deg_5 = false;
		boolean deg_10 = false;
		boolean deg_20 = false;
		boolean deg_30 = false;
		boolean deg_50 = false;
		
		for (int i = 1; i <= 1000; i++) {
			for (int j = 1; j <= 1000; j++) { 
				degradeImage (newImage, i * 0.01f, j * 0.01f);
				double nrmse = getNRMSE(image, newImage);
				
				count++;
				
				// Code to save the image for degradation 1%
				if (nrmse >= 0.01 && nrmse <= 0.011 && !deg_1) 
				{ 
					System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
				   	deg_1 = true;
				   
				   	double psnr = getPSNR(image, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						imageSaver.save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						imageSaver.save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
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
				   
				   	double psnr = getPSNR(image, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						imageSaver.save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						imageSaver.save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
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
				   
				   	double psnr = getPSNR(image, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						imageSaver.save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						imageSaver.save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
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
				   
				   	double psnr = getPSNR(image, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						imageSaver.save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						imageSaver.save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
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
				   
				   	double psnr = getPSNR(image, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						imageSaver.save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						imageSaver.save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
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
				   
				   	double psnr = getPSNR(image, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						imageSaver.save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						imageSaver.save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
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
				   
				   	double psnr = getPSNR(image, newImage);
					if (mode.equalsIgnoreCase("nrmse")) {
						imageSaver.save("_" + (double)((int)(nrmse * 1000) / 1000.0) + ".rgb", newImage);
					}	
					else if (mode.equalsIgnoreCase("psnr"))
						imageSaver.save("_" + (double)((int)(psnr * 1000) / 1000.0) + ".rgb", newImage);
					else {
						System.out.println("Error: Unknown mode!");
						System.exit(0);
					}
				}
				
				if(deg_1 && deg_3 && deg_5 && deg_10 && deg_20 && deg_30/* && deg_50*/)
					return;

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
}
