package dev.practice.assessment03.error;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.MethodArgumentNotValidException;
@RestControllerAdvice
public class ApiExceptionHandler {
 @ExceptionHandler(ApiException.class) ResponseEntity<ApiError> domain(ApiException e,HttpServletRequest r){return response(e.status(),e.code(),e.getMessage(),r);}
 @ExceptionHandler({HttpMessageNotReadableException.class,MethodArgumentTypeMismatchException.class,MissingServletRequestParameterException.class,MethodArgumentNotValidException.class})
 ResponseEntity<ApiError> invalid(Exception e,HttpServletRequest r){return response(400,"INVALID_REQUEST","Invalid request",r);}
 @ExceptionHandler(Exception.class) ResponseEntity<ApiError> unexpected(Exception e,HttpServletRequest r){return response(500,"INTERNAL_ERROR","Request could not be completed",r);}
 private ResponseEntity<ApiError> response(int s,String c,String m,HttpServletRequest r){return ResponseEntity.status(s).body(new ApiError(s,c,m,r.getRequestURI()));}
}
