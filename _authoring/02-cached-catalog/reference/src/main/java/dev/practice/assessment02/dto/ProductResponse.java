package dev.practice.assessment02.dto;
import dev.practice.assessment02.model.Product;
public record ProductResponse(long id,String sku,String name,String category,int priceCents,int stock){
 public static ProductResponse from(Product p){return new ProductResponse(p.getId(),p.getSku(),p.getName(),p.getCategory(),p.getPriceCents(),p.getStock());}
}
