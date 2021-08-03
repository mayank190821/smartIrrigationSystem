package com.logic_api.smartirrigation;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import com.google.firebase.FirebaseException;
import com.google.firebase.auth.*;
import java.util.Objects;
import java.util.concurrent.TimeUnit;

public class AuthenticationActivity extends AppCompatActivity {

    private FirebaseAuth firebaseAuth;

    String verificationCodeBySystem;
    Button nextButton, sendButton;
    EditText phone;
    EditText otp;


    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_authentication);

        firebaseAuth = FirebaseAuth.getInstance();

        nextButton = findViewById(R.id.nextButton);
        phone = findViewById(R.id.phone);
        otp = findViewById(R.id.otp);
        sendButton = findViewById(R.id.sendButton);
        sendButton.setOnClickListener(view -> sendVerificationCodeToUser(phone.getText().toString()));
        nextButton.setOnClickListener(view -> verifyCode(otp.getText().toString()));
    }

    private void sendVerificationCodeToUser(String phoneNo) {
        String number = "+91"+phoneNo;
        PhoneAuthProvider.getInstance().verifyPhoneNumber(
                number,
                60,
                TimeUnit.SECONDS,
                AuthenticationActivity.this,
                mCallbacks
        );
    }

    private final PhoneAuthProvider.OnVerificationStateChangedCallbacks mCallbacks = new PhoneAuthProvider.OnVerificationStateChangedCallbacks() {

        @Override
        public void onCodeSent(@NonNull String s, @NonNull PhoneAuthProvider.ForceResendingToken forceResendingToken) {
            super.onCodeSent(s, forceResendingToken);
            verificationCodeBySystem = s;
        }

        @Override
        public void onVerificationCompleted(@NonNull PhoneAuthCredential phoneAuthCredential) {
            String code = phoneAuthCredential.getSmsCode();
            if(code != null) {
                verifyCode(code);
            }
        }

        @Override
        public void onVerificationFailed(@NonNull FirebaseException e) {
            Toast.makeText(AuthenticationActivity.this, "failed", Toast.LENGTH_SHORT).show();
        }
    };

    private void verifyCode(String code) {
        PhoneAuthCredential credential = PhoneAuthProvider.getCredential(verificationCodeBySystem, code);
        signInUserByCredentials(credential);
    }

    private void signInUserByCredentials(PhoneAuthCredential credential) {
        firebaseAuth.signInWithCredential(credential)
                .addOnCompleteListener(AuthenticationActivity.this, task -> {
                    if(task.isSuccessful()){
                        Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                        startActivity(intent);

                    }
                    else{
                        Toast.makeText(AuthenticationActivity.this, Objects.requireNonNull(task.getException()).getMessage(), Toast.LENGTH_SHORT).show();
                    }
                });
    }
}



