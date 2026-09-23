package dev.practice.assessment03.service;
import org.springframework.stereotype.Component;import dev.practice.assessment03.error.InsufficientStockException;
@Component public class AvailabilityChecker {public void check(int available,int requested){if(available < requested)throw new InsufficientStockException();}}
