package dev.practice.assessment02.support;
import org.springframework.boot.test.context.TestConfiguration;import org.springframework.context.annotation.*;
@TestConfiguration public class ClockTestConfig {@Bean @Primary public MutableClock testClock(){return new MutableClock();}}
