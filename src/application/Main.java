package application;
	
import javafx.application.Application;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;

public class Main extends Application {
	
	private AnchorPane rootLayout;
	private static Stage primaryStage;
	@FXML
	private ImageView origin_iv;
	
	public static Stage getPrimaryStage() {
		return primaryStage;
	}

	@Override
	public void start(Stage primaryStage) {
		try {
			// Load root layout from fxml file.
            FXMLLoader loader = new FXMLLoader();
            loader.setLocation(Main.class.getResource("MainScene.fxml"));
            rootLayout = (AnchorPane) loader.load();
			
			Scene scene = new Scene(rootLayout);
			this.primaryStage = primaryStage;
			primaryStage.setScene(scene);
			primaryStage.setTitle("Painting Identification");
			primaryStage.show();
			
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		launch(args);
	}
	
}
