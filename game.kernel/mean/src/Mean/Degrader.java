package Mean;

import java.io.IOException;
import java.util.Random;

public class Degrader {
	
	public int width;
	public int height;
	public int[][][] image;
	public String mode;
	public double errorRange;
	
	Degrader(int width, int height, int[][][] orgImage, String mode, double errorRange) {
		System.out.println("width: " + width);
		this.width = width;
		this.height = height;
		initImage(orgImage);
		this.mode = mode;
		this.errorRange = errorRange;
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
	
	public void degrade (double[] errors, ImageSaver imageSaver) throws IOException {
		int[][][] newImage;
		newImage = new int[height][][];
		for (int i=0; i<height; i++){
			newImage[i] = new int[width][];
			for(int j=0; j<width; j++){
				newImage[i][j] = new int[3];
			}
		}
		
		Random r = new Random();
		for (int errIdx = 0; errIdx < errors.length; errIdx++) {
			
			for (int i=0; i<height; i++) {
				for (int j=0; j<width; j++) {
					for (int k=0; k<3; k++) {
						newImage[i][j][k] = image[i][j][k];
					}
				}
			}
			
			boolean find = false;
			int h, w, diff;
			double sum = 0.0;
			int count = 0; //debug
			
			if (mode.equalsIgnoreCase("nrmse")) {
				double nrmse;
				do {
					count++;
					
					h = (int)(r.nextDouble() * height);
					w = (int)(r.nextDouble() * width);
					
					newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = r.nextInt(255);
					
					diff = Math.abs(newImage[h][w][0] - image[h][w][0]);
					sum += diff * diff;
					nrmse = Math.sqrt(sum / (height * width)) / 255.0;
					
					if (nrmse > errors[errIdx] && nrmse < errors[errIdx] + errorRange) {
						find = true;
						imageSaver.save("_" + errors[errIdx] + ".rgb", newImage);
						System.out.println("NRMSE: " + nrmse + "\tCount: " + count);
					}
				} while (!find);	
			} else if (mode.equalsIgnoreCase("psnr")) {
				double mse, psnr;
				do {
					count++;
					
					h = (int)(r.nextDouble() * height);
					w = (int)(r.nextDouble() * width);
					
					newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = r.nextInt(255);
					
					diff = Math.abs(newImage[h][w][0] - image[h][w][0]);
					sum += diff * diff;
					mse = sum / (height * width);
					psnr = 10 * Math.log10(255.0 * 255.0 / mse); 
					
					if (psnr > errors[errIdx] && psnr < errors[errIdx] + errorRange) {
						find = true;
						imageSaver.save("_" + errors[errIdx] + ".rgb", newImage);
						System.out.println("NRMSE: " + psnr + "\tCount: " + count);
					}
				} while (!find);	
			} else {
				System.out.println("Error: Unknown mode!");
				System.exit(0);
			}
		}
	}
}
