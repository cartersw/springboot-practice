package dev.practice.assessment03.error;
public class InvalidRequestException extends ApiException {
 public InvalidRequestException(String message){super(400,"INVALID_REQUEST",message);}
}
