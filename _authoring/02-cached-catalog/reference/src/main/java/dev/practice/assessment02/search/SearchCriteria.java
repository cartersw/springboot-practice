package dev.practice.assessment02.search;
public record SearchCriteria(String q,String category,Integer minPrice,Integer maxPrice,Boolean inStock,int page,int size,SearchSort sort) {}
