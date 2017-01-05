package Jpeg;

import java.io.IOException;
import java.util.StringTokenizer;

import Jpeg.TextFile.Mode;

public class ImageSaver {
	public int width;
	public int height;
	
	public String inputFilePath;
	public String outDirPath;
	public String mode;
	
	ImageSaver (int width, int height, String mode, String inputFilePath, String outDirPath) {
		this.width = width;
		this.height = height;
		this.mode = mode;
		this.inputFilePath = inputFilePath;
		this.outDirPath = outDirPath;
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
}
