package Emboss;

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
	
	int getWrongPixels(int[][][] image1, int[][][] image2){
		int cnt = 0;
		for (int i=0; i<height; i++){
			for (int j=0; j<width; j++){
				if (image1[i][j][0] != image2[i][j][0] || image1[i][j][1] != image2[i][j][1] || image1[i][j][2] != image2[i][j][2]) {
					cnt++;
				}
			}
		}
		return cnt;
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
		int orgValue;
		
		int count = 0; //debug
		
		int max = -1;
		int min = 256;
		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {
				if (image[i][j][0] > max)
					max = image[i][j][0];
				if (image[i][j][0] < min)
					min = image[i][j][0];
			}
		}
		
		if (mode.equalsIgnoreCase("nrmse")) {
			double nrmse;
			do {
				count++;
				
				h = (int)(r.nextDouble() * height);
				w = (int)(r.nextDouble() * width);
				
				orgValue = newImage[h][w][0];
				
				if (w == width-1) 
					newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h][w-1][0];
				else if (w == 0) 
					newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h][w+1][0];
				else if (h == height-1) 
					newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h-1][w][0];
				else if (h == 0) 
					newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h+1][w][0];
				else {
					double rd = r.nextDouble();
					if (rd < 0.25)
						newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h][w-1][0];
					else if (rd >= 0.25 && rd < 0.5)
						newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h][w+1][0];
					else if (rd >= 0.5 && rd < 0.75)
						newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h-1][w][0];
					else
						newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = newImage[h+1][w][0];
				}
				
				diff = Math.abs(newImage[h][w][0] - image[h][w][0]);
				String key = String.valueOf(h) + 'x' + String.valueOf(w); 
				if (diffMap.containsKey(key)) {
					val = diffMap.get(key);
					if (val < diff || r.nextDouble() > 0.05) {
						sum -= val * val;
						diffMap.put(key, diff);
						sum += diff * diff;
					} else {
						newImage[h][w][0] = newImage[h][w][1] = newImage[h][w][2] = orgValue;
					}
				} else {
					diffMap.put(key, diff);
					sum += diff * diff;
				}
				nrmse = Math.sqrt(sum / (height * width)) / (max - min);
				
				if (nrmse > errors[errIdx] && nrmse < errors[errIdx] + errorRange) {
					imageSaver.save("_" + errors[errIdx] + ".rgb", newImage);
					System.out.println("File[" + path + "]    NRMSE: " + nrmse + "\tCount: " + count);
					numFound++;
					long sum2 = 0;
					for (int i=0; i < height; i++){
						for (int j=0; j < width; j++){
							diff = Math.abs(newImage[i][j][0] - image[i][j][0]);
							sum2 += diff * diff;
						}
					}
//					System.out.println("sum2: " + sum2);
					System.out.println("Real NRMSE: " + Math.sqrt(sum2 / (height * width)) / (max - min));
					System.out.println("Skipped," + errors[errIdx] + "," + getWrongPixels(image, newImage));
					if (numFound == errors.length)
						find = true;
					errIdx++;
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
