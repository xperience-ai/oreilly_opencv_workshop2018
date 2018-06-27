package ai.xperience.samples.facerecognition;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

class AsyncRecognizer extends AsyncTask<String, Void, String> {
    private static final String    TAG                 = "Xperience.AI::FR";
    private String response;
    private Context context;

    public AsyncRecognizer(Context _context) {
        context = _context;
    }

    @Override
    protected String doInBackground(String... params) {
        String server = params[0];
        String encodedImage = params[1];
        Log.i(TAG, "Full HTTP request: " + server);

        try {
            URL obj = new URL(server);
            HttpURLConnection connection = (HttpURLConnection) obj.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("User-Agent", "Android Client");

            OutputStream os = connection.getOutputStream();
            os.write(encodedImage.getBytes("UTF-8"));
            os.close();

            int responseCode = connection.getResponseCode();
            Log.i(TAG, "HTTP response code: " + responseCode);

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuffer responseBuffer = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                responseBuffer.append(inputLine);
            }
            in.close();

            response = responseBuffer.toString();
        } catch(IOException e) {
            e.printStackTrace();
        }

        return null;
    }

    @Override
    protected void onPostExecute(String result) {
        Toast toast = Toast.makeText(context, response, Toast.LENGTH_SHORT);
        toast.show();
    }
}
