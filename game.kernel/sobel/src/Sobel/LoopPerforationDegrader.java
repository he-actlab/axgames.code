package Sobel;

import java.io.IOException;
import java.util.HashMap;
import java.util.Random;

public class LoopPerforationDegrader {
	
	public int width;
	public int height;
	public int[][][] image;
	public String mode;
	public double errorRange;
	public String path;
	
	LoopPerforationDegrader(int width, int height, int[][][] orgImage, String mode, double errorRange, String path) {
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
		int diff, val;
		int errIdx = 0;
		int numFound = 0;
		long sum = 0;
		double lasterror = 0.0;
		HashMap<String, Integer> diffMap = new HashMap<String, Integer>();
		
		int count = 0; //debug
		
		int mean, meansum = 0;
		int max = -1;
		int min = 256;
		for (int i = 0; i < height; i++) {
			for (int j = 0; j < width; j++) {
				meansum += image[i][j][0];
				if (image[i][j][0] > max)
					max = image[i][j][0];
				if (image[i][j][0] < min)
					min = image[i][j][0];
			}
		}
		mean = meansum / (height * width);
		
		if (mode.equalsIgnoreCase("nrmse")) {
			double nrmse;
			for (int jump = 2; jump < width; jump++){
				System.out.println("jump = " + jump);
				for (int h = 0; h < height; h++) {
					for (int w = 0; w < width; w += jump) {
						for (int k = 1; k < jump; k++) {
							if (w + k >= width)
								continue;
							count++;
							newImage[h][w + k][0] = newImage[h][w + k][1] = newImage[h][w + k][2] = image[h][w][0];
							diff = Math.abs(newImage[h][w][0] - image[h][w][0]);
							String key = String.valueOf(h) + 'x' + String.valueOf(w); 
							if (diffMap.containsKey(key)) {
								val = diffMap.get(key);
								sum -= val * val;
							} 
							diffMap.put(key, diff);
							sum += diff * diff;
							nrmse = Math.sqrt(sum / (height * width)) / (max - min);
							System.out.println("NRMSE: " + nrmse);
							if (nrmse > errors[errIdx] && nrmse < errors[errIdx] + errorRange) {
								imageSaver.save("_" + errors[errIdx] + ".rgb", newImage);
								System.out.println("File[" + path + "]    NRMSE: " + nrmse + "\tCount: " + count);
								lasterror = errors[errIdx];
								errIdx++;
								numFound++;
								if (numFound == errors.length) {
									find = true;
									break;
								}
							}
						}							
						if (find == true)
							break;
					}
					if(find == true)
						break;
				}
				if(find == true)
					break;
			}
			for (int i = (int)(lasterror * 100); i < (int)(errors[errors.length-1] * 100); i++) {
				imageSaver.save("_" + errors[i] + ".rgb", newImage);
			}	
		} 
		else {
			System.out.println("Error: Unknown mode!");
			System.exit(0);
		}
	}
}
