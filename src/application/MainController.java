package application;

import java.awt.List;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import javax.imageio.ImageIO;

import javafx.embed.swing.SwingFXUtils;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;

public class MainController {
	
	File imagefile;
	Image originImage;
	@FXML
	ImageView origin_iv;
	@FXML
	VBox side_bar;
	
	@FXML
	private void upload_image(ActionEvent event) {
		event.consume();
		System.out.println("Upload Btn Clicked!");
		
		FileChooser fileChooser = new FileChooser();
		fileChooser.setTitle("Open Resource File");
		imagefile = fileChooser.showOpenDialog(Main.getPrimaryStage());
		originImage = readImageByFile(imagefile);
		
		origin_iv.setImage(originImage);
		
		side_bar.getChildren().clear();//清空侧边栏
	}
	
	@FXML
	private void process1(ActionEvent event) {
		event.consume();
		System.out.println("Proc1 Btn Clicked!");
		
		//Painting processing
		ArrayList<String> stampPathList = pyStampSegmentation(imagefile);
		for (String stampPath:stampPathList) {//将分割后的印章图像文件逐一读取放入界面
			System.out.println(stampPath);
			Image stampImage = readImageByFile(new File(stampPath));
			ImageView imageView = new ImageView(stampImage);
			imageView.maxHeight(400);
			imageView.setPreserveRatio(true);
			side_bar.getChildren().add(imageView);
			Label label = new Label(stampPath);
			side_bar.getChildren().add(label);
		}
		
		
	}
	
	private Image readImageByFile(File imagefile) {
		Image image = null;
		if(imagefile!=null) {
			try {
				BufferedImage bufferedImage = ImageIO.read(imagefile);
				image = SwingFXUtils.toFXImage(bufferedImage , null);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}else {
			System.out.println("Open image file failed!");
			return null;
		}
		return image;
	}
	
	private ArrayList<String> pyStampSegmentation (File inputFile) {
		ArrayList<String> resultList = new ArrayList<String>();
		String inputFilePath = inputFile.getPath();
		System.out.println(inputFilePath);
		try {
			//图片路径作为参数运行 python 脚本
			String[] pythonArgs = new String[] {"python", ".\\stamp.py", inputFilePath};
			Process proc = Runtime.getRuntime().exec(pythonArgs);
			 // 定义Python脚本的返回值
            String result = null;
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                result = line;
                //System.out.println(result);
                resultList.add(result);
            }
            in.close();
			proc.waitFor();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return resultList;
	}
}
