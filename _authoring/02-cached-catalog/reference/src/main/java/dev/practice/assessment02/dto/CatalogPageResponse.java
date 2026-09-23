package dev.practice.assessment02.dto;
import java.util.List;
public record CatalogPageResponse(List<ProductResponse> content,int page,int size,long totalElements,int totalPages,boolean first,boolean last){
 public CatalogPageResponse {content=List.copyOf(content);}
}
