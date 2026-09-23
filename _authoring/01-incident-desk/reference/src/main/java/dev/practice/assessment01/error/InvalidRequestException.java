package dev.practice.assessment01.error;
public class InvalidRequestException extends ApiException {
 public InvalidRequestException(String message){super(400,"INVALID_REQUEST",message);}
}
