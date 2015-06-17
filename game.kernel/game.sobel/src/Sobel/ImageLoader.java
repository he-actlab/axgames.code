package Sobel;

import java.io.IOException;
import java.util.StringTokenizer;

import Sobel.TextFile.Mode;

public class ImageLoader {
	public int width;
	public int height;
	
	public String inputFilePath;
	public String outDirPath;
	public String mode;
	
	public int[][][] image;
	
	ImageLoader (String mode, String inputFilePath, String outDirPath) {
		this.mode = mode;
		this.inputFilePath = inputFilePath;
		this.outDirPath = outDirPath;
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
	
	public int[][][] getImage() {
		return image;
	}
	
	public int getWidth() {
		return width;
	}

	public int getHeight() {
		return height;
	}
}
