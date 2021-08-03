package com.logic_api.smartirrigation;

import android.content.Intent;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.os.Handler;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class WelcomeActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);
        FirebaseUser currentUser = FirebaseAuth.getInstance().getCurrentUser();

        new Handler().postDelayed(() -> {
            Intent intent;
            if (currentUser != null) {
                intent = new Intent(getApplicationContext(), MainActivity.class);
            }
            else{
                intent = new Intent(getApplicationContext(), AuthenticationActivity.class);
            }
            startActivity(intent);
            finish();
        }, 2000);
    }
}