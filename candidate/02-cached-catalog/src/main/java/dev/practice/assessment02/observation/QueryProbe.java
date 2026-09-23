package dev.practice.assessment02.observation;
import java.util.concurrent.atomic.AtomicLong;import org.springframework.stereotype.Component;
@Component public class QueryProbe {private final AtomicLong count=new AtomicLong();public long calls(){return count.get();}public void reset(){count.set(0);}void increment(){count.incrementAndGet();}}
