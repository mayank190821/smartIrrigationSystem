package com.logic_api.smartirrigation;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import java.util.Objects;

public class MainActivity extends AppCompatActivity{

    int moisture = 0, temperature=0, humidity=0;
    String longitude="50.77°E", latitude="340.56°N";
    ProgressBar moistureProgress, humidityProgress, temperatureProgress;
    TextView moistureValue, temperatureValue, humidityValue, vLongitude, vLatitude;
    ImageButton imageButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        moistureProgress = findViewById(R.id.progress1);
        humidityProgress = findViewById(R.id.progress2);
        temperatureProgress = findViewById(R.id.progress3);
        vLongitude = findViewById(R.id.longitude);
        vLatitude = findViewById(R.id.latitude);
        moistureValue = findViewById(R.id.value1);
        humidityValue = findViewById(R.id.value2);
        temperatureValue = findViewById(R.id.value3);
        imageButton = findViewById(R.id.imageButton);

        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference myRef = database.getReference();

        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                moisture = Integer.parseInt(Objects.requireNonNull(snapshot.child("moisture").getValue(String.class)));
                temperature = Integer.parseInt(Objects.requireNonNull(snapshot.child("temperature").getValue(String.class)));
                humidity = Integer.parseInt(Objects.requireNonNull(snapshot.child("humidity").getValue(String.class)));
                longitude = snapshot.child("longitude").getValue(String.class);
                latitude = snapshot.child("latitude").getValue(String.class);
                updateData();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });

        updateData();

        imageButton.setOnClickListener(view -> {
                FirebaseAuth.getInstance().signOut();
                startActivity(new Intent(getApplicationContext(), AuthenticationActivity.class));
                finish();
        });
    }

    private void updateData() {
        moistureProgress.setProgress(moisture);
        String textValue = moisture + "%";
        moistureValue.setText(textValue);

        temperatureProgress.setProgress(temperature);
        textValue = temperature + "°C";
        temperatureValue.setText(textValue);

        humidityProgress.setProgress(humidity);
        textValue = humidity + "%";
        humidityValue.setText(textValue);

        textValue = "Longitude : " + longitude;
        vLongitude.setText(textValue);
        textValue = "Latitude : " + latitude;
        vLatitude.setText(textValue);
    }
}