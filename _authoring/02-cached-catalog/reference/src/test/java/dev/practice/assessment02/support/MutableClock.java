package dev.practice.assessment02.support;
import java.time.*;
public class MutableClock extends Clock {private Instant now=Instant.parse("2030-01-01T00:00:00Z");public void reset(){now=Instant.parse("2030-01-01T00:00:00Z");}public void advance(long seconds){now=now.plusSeconds(seconds);}public ZoneId getZone(){return ZoneOffset.UTC;}public Clock withZone(ZoneId zone){return this;}public Instant instant(){return now;}}
