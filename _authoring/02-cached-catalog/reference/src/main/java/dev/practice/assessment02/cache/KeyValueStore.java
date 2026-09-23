package dev.practice.assessment02.cache;
import java.util.*;import java.time.Duration;
public interface KeyValueStore {Optional<String> get(String key);void put(String key,String value,Duration ttl);void delete(String key);Set<String> keys();}
