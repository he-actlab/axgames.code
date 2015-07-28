package Jpeg;

import java.io.IOException;
import java.util.HashMap;
import java.util.Random;

public class TileDegrader {
	
	public int width;
	public int height;
	public int[][][] image;
	public String mode;
	public double errorRange;
	public String path;
	
	TileDegrader(int width, int height, int[][][] orgImage, String mode, double errorRange, String path) {
		System.out.println("width: " + width);
		this.width = width;
		this.height = height;
		initImage(orgImage);
		this.mode = mode;
		this.errorRange = errorRange;
		this.path = path;
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
	
	private int euclideanNorm(int[] rgb) {
		return (int)(Math.sqrt(Math.pow(rgb[0], 2) + Math.pow(rgb[1], 2) + Math.pow(rgb[2], 2)));
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
		for (int i=0; i<height; i++) {
			for (int j=0; j<width; j++) {
				for (int k=0; k<3; k++) {
					newImage[i][j][k] = image[i][j][k];
				}
			}
		}
		
		boolean find = false;
		int h, w, diff, val;
		int errIdx = 0;
		int numFound = 0;
		long sum = 0;
		HashMap<String, Integer> diffMap = new HashMap<String, Integer>();
		int[] orgValue = new int[3];
		int orgNorm, newNorm;
		
		int count = 0; //debug
		
		int max = -1;
		int min = 10000000;
		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {
				int euc = euclideanNorm(image[i][j]);
				if (euc > max)
					max = euc;
				if (euc < min)
					min = euc;
			}
		}
		
		if (mode.equalsIgnoreCase("nrmse")) {
			double nrmse;
			do {
				count++;
				
				h = (int)(r.nextDouble() * height);
				w = (int)(r.nextDouble() * width);
				
				orgValue[0] = newImage[h][w][0];
				orgValue[1] = newImage[h][w][1];
				orgValue[2] = newImage[h][w][2];
				
				if (w == width-1) {
					newImage[h][w][0] = newImage[h][w-1][0];
					newImage[h][w][1] = newImage[h][w-1][1];
					newImage[h][w][2] = newImage[h][w-1][2];
				} else if (w == 0) {
					newImage[h][w][0] = newImage[h][w+1][0];
					newImage[h][w][1] = newImage[h][w+1][1];
					newImage[h][w][2] = newImage[h][w+1][2];
				} else if (h == height-1) { 
					newImage[h][w][0] = newImage[h-1][w][0];
					newImage[h][w][1] = newImage[h-1][w][1];
					newImage[h][w][2] = newImage[h-1][w][2];
				} else if (h == 0) { 
					newImage[h][w][0] = newImage[h+1][w][0];
					newImage[h][w][1] = newImage[h+1][w][1];
					newImage[h][w][2] = newImage[h+1][w][2];
				} else {
					double rd = r.nextDouble();
					if (rd < 0.25) {
						newImage[h][w][0] = newImage[h][w-1][0];
						newImage[h][w][1] = newImage[h][w-1][1];
						newImage[h][w][2] = newImage[h][w-1][2];
					} else if (rd >= 0.25 && rd < 0.5) {
						newImage[h][w][0] = newImage[h][w+1][0];
						newImage[h][w][1] = newImage[h][w+1][1];
						newImage[h][w][2] = newImage[h][w+1][2];
					} else if (rd >= 0.5 && rd < 0.75) {
						newImage[h][w][0] = newImage[h-1][w][0];
						newImage[h][w][1] = newImage[h-1][w][1];
						newImage[h][w][2] = newImage[h-1][w][2];
					} else {
						newImage[h][w][0] = newImage[h+1][w][0];
						newImage[h][w][1] = newImage[h+1][w][1];
						newImage[h][w][2] = newImage[h+1][w][2];
					}	
				}
				
				orgNorm = euclideanNorm(image[h][w]);
				newNorm = euclideanNorm(newImage[h][w]);
				diff = Math.abs(orgNorm - newNorm);
				String key = String.valueOf(h) + 'x' + String.valueOf(w); 
				if (diffMap.containsKey(key)) {
					val = diffMap.get(key);
					if (val < diff || r.nextDouble() > 0.1) {
						sum -= val * val;
						diffMap.put(key, diff);
						sum += diff * diff;
					} else {
						newImage[h][w][0] = orgValue[0];
						newImage[h][w][1] = orgValue[1];
						newImage[h][w][2] = orgValue[2];
					}
				} else {
					diffMap.put(key, diff);
					sum += diff * diff;
				}
				nrmse = Math.sqrt(sum / (height * width)) / (max - min);
				
				if (nrmse > errors[errIdx] && nrmse < errors[errIdx] + errorRange) {
					imageSaver.save("_" + errors[errIdx] + ".rgb", newImage);
					System.out.println("File[" + path + "]    NRMSE: " + nrmse + "\tCount: " + count);
					errIdx++;
					numFound++;
					long sum2 = 0;
					for (int i=0; i < height; i++){
						for (int j=0; j < width; j++){
							orgNorm = euclideanNorm(image[i][j]);
							newNorm = euclideanNorm(newImage[i][j]);
							diff = Math.abs(orgNorm - newNorm);
							sum2 += diff * diff;
						}
					}
//					System.out.println("sum2: " + sum2);
					System.out.println("Real NRMSE: " + Math.sqrt(sum2 / (height * width)) / (max - min));
					if (numFound == errors.length)
						find = true;
				}
			} while (!find);	
		} 
		else if (mode.equalsIgnoreCase("psnr")) {
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
					imageSaver.save("_" + errors[errIdx] + ".rgb", newImage);
					System.out.println("NRMSE: " + psnr + "\tCount: " + count);
					errIdx++;
					numFound++;
					if (numFound == errors.length)
						find = true;
				}
			} while (!find);	
		} else {
			System.out.println("Error: Unknown mode!");
			System.exit(0);
		}
	}
}
