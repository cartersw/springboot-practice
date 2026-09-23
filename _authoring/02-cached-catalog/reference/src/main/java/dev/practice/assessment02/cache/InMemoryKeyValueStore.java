package dev.practice.assessment02.cache;
import java.util.*;import java.time.*;
import org.springframework.stereotype.Component;
@Component public class InMemoryKeyValueStore implements KeyValueStore {
 private record Entry(String value,Instant expiresAt){}
 private final Map<String,Entry> entries=new HashMap<>();private final Clock clock;
 public InMemoryKeyValueStore(Clock c){clock=c;}
 public synchronized Optional<String> get(String key){Entry e=entries.get(key);if(e==null)return Optional.empty();if(!clock.instant().isBefore(e.expiresAt())){entries.remove(key);return Optional.empty();}return Optional.of(e.value());}
 public synchronized void put(String k,String v,Duration ttl){entries.put(k,new Entry(v,clock.instant().plus(ttl)));}
 public synchronized void delete(String k){entries.remove(k);}
 public synchronized Set<String> keys(){for(String k:new HashSet<>(entries.keySet()))get(k);return new HashSet<>(entries.keySet());}
}
