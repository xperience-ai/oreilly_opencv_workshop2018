package ai.xperience.samples.facerecognition;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import android.util.Base64;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewFrame;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.CameraBridgeViewBase.CvCameraViewListener2;
import org.opencv.dnn.Net;
import org.opencv.dnn.Dnn;

import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.WindowManager;

import static org.opencv.imgcodecs.Imgcodecs.imencode;

public class FaceRecognition extends AppCompatActivity implements CvCameraViewListener2 {

    private static final String    TAG                 = "Xperience.AI::FR";

    private static final int inWidth = 300;
    private static final int inHeight = 300;
    private static final Size inSize = new Size(inWidth, inHeight);
    private static final Scalar mean = new Scalar(104, 117, 123, 0);
    private static final Scalar FACE_COLOR = new Scalar(0, 255, 0);

    private MenuItem mItemIntroduce;
    private MenuItem mItemRecognize;

    private Mat                    mRgba;
    private Mat                    mBlob;
    private Mat                    mLastFace;
    private File                   mProtoFile;
    private File                   mModelFile;
    private Net                    mDetector;

    private CameraBridgeViewBase   mOpenCvCameraView;

    private File prepareRawResource(int id, String fileName) throws IOException {
        InputStream is = getResources().openRawResource(id);
        File modelDir = getDir("model", Context.MODE_PRIVATE);

        File result = new File(modelDir, fileName);
        FileOutputStream os = new FileOutputStream(result);

        byte[] buffer = new byte[4096];
        int bytesRead;
        while ((bytesRead = is.read(buffer)) != -1) {
            os.write(buffer, 0, bytesRead);
        }
        is.close();
        os.close();

        return result;
    }

    private BaseLoaderCallback  mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS:
                {
                    Log.i(TAG, "OpenCV loaded successfully");

                    try {
                        mProtoFile = prepareRawResource(R.raw.prototxt, "deploy.prototxt");
                        Log.i(TAG, "Copied model deploy.txt");
                        mModelFile = prepareRawResource(R.raw.caffemodel, "res10_300x300_ssd_iter_140000_fp16.caffemodel");
                        Log.i(TAG, "Copied model res10_300x300_ssd_iter_140000_fp16.caffemodel");
                        mDetector = Dnn.readNetFromCaffe(mProtoFile.getAbsolutePath(), mModelFile.getAbsolutePath());
                        Log.i(TAG, "Created detector net");
                        if (mDetector.empty()) {
                            Log.e(TAG, "Failed to load Dnn model");
                            mDetector = null;
                        } else
                            Log.i(TAG, "Loaded model " + mProtoFile.getAbsolutePath());

                    } catch (IOException e) {
                        e.printStackTrace();
                        Log.e(TAG, "Failed to load cascade. Exception thrown: " + e);
                    }

                    mOpenCvCameraView.enableView();
                } break;
                default:
                {
                    super.onManagerConnected(status);
                } break;
            }
        }
    };

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        Log.i(TAG, "called onCreate");
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        setContentView(R.layout.activity_face_recognition);

        mOpenCvCameraView = findViewById(R.id.face_detection_view);
        mOpenCvCameraView.setVisibility(CameraBridgeViewBase.VISIBLE);
        mOpenCvCameraView.setCvCameraViewListener(this);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        Log.i(TAG, "called onCreateOptionsMenu");
        mItemIntroduce = menu.add("Introduce");
        mItemRecognize = menu.add("Recognize");
        return true;
    }

    public boolean onOptionsItemSelected(MenuItem item) {
        Log.i(TAG, "called onOptionsItemSelected; selected item: " + item);
        if(mLastFace.empty())
            return true;

        if (item == mItemIntroduce) {

        } else if (item == mItemRecognize) {
            MatOfByte encodedFace = new MatOfByte();
            imencode(".png", mLastFace, encodedFace);
            String encodedFaceBase64 = "data:image/png;base64," +
                    Base64.encodeToString(encodedFace.toArray(), Base64.DEFAULT);
            try {
                AsyncRecognizer rec = new AsyncRecognizer(getApplicationContext());
                rec.execute("http://192.168.32.61:8080/recognize", encodedFaceBase64);
                Log.i(TAG, "Sent HTTP Request");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return true;
    }

    @Override
    public void onPause()
    {
        super.onPause();
        if (mOpenCvCameraView != null)
            mOpenCvCameraView.disableView();
    }

    @Override
    public void onResume()
    {
        super.onResume();
        if (!OpenCVLoader.initDebug()) {
            Log.d(TAG, "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, mLoaderCallback);
        } else {
            Log.d(TAG, "OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }
    }

    public void onDestroy() {
        super.onDestroy();
        mOpenCvCameraView.disableView();
    }

    public void onCameraViewStarted(int width, int height) {
        mRgba = new Mat();
        mLastFace = new Mat();
    }

    public void onCameraViewStopped() {
        mRgba.release();
        mLastFace.release();
    }

    public Mat onCameraFrame(CvCameraViewFrame inputFrame) {
        Log.i(TAG, "New camera frame");
        mRgba = inputFrame.rgba();
        Mat rgb = new Mat();

        Imgproc.cvtColor(mRgba, rgb, Imgproc.COLOR_BGRA2BGR);

        if (mDetector != null) {
            mBlob = Dnn.blobFromImage(rgb, 1.0, inSize, mean, true, false);
            Log.i(TAG, "Created input blob");
            mDetector.setInput(mBlob, "data");

            Mat detections = mDetector.forward("detection_out");
            Log.i(TAG, "After net.forward()");

            int cols = mRgba.cols();
            int rows = mRgba.rows();
            detections = detections.reshape(1, (int) detections.total() / 7);
            for (int i = 0; i < detections.rows(); ++i) {
                double confidence = detections.get(i, 2)[0];
                if (confidence > 0.5) {
                    int xLeftBottom = (int) (detections.get(i, 3)[0] * cols);
                    int yLeftBottom = (int) (detections.get(i, 4)[0] * rows);
                    int xRightTop = (int) (detections.get(i, 5)[0] * cols);
                    int yRightTop = (int) (detections.get(i, 6)[0] * rows);
                    Rect object = new Rect(xLeftBottom, yLeftBottom,
                            xRightTop - xLeftBottom,
                            yRightTop - yLeftBottom);

                    mLastFace = mRgba.submat(object);
                    // Draw rectangle around detected object.
                    Imgproc.rectangle(mRgba, new Point(xLeftBottom, yLeftBottom),
                            new Point(xRightTop, yRightTop), FACE_COLOR);
                }
            }
        }

        return mRgba;
    }
}
