import 'package:json_annotation/json_annotation.dart';
import 'blog_post.dart';

part 'search_result.g.dart';

@JsonSerializable()
class SearchSuggestion {
  final String text;
  final String type;
  final String description;

  const SearchSuggestion({
    required this.text,
    required this.type,
    required this.description,
  });

  factory SearchSuggestion.fromJson(Map<String, dynamic> json) => 
      _$SearchSuggestionFromJson(json);
  Map<String, dynamic> toJson() => _$SearchSuggestionToJson(this);
}

@JsonSerializable()
class SearchFilters {
  final List<CategoryFilter> categories;
  final List<TagFilter> tags;
  final List<AuthorFilter> authors;

  const SearchFilters({
    required this.categories,
    required this.tags,
    required this.authors,
  });

  factory SearchFilters.fromJson(Map<String, dynamic> json) => 
      _$SearchFiltersFromJson(json);
  Map<String, dynamic> toJson() => _$SearchFiltersToJson(this);
}

@JsonSerializable()
class CategoryFilter {
  final String name;
  final String slug;

  const CategoryFilter({
    required this.name,
    required this.slug,
  });

  factory CategoryFilter.fromJson(Map<String, dynamic> json) => 
      _$CategoryFilterFromJson(json);
  Map<String, dynamic> toJson() => _$CategoryFilterToJson(this);
}

@JsonSerializable()
class TagFilter {
  final String name;
  @JsonKey(name: 'post_count')
  final int postCount;

  const TagFilter({
    required this.name,
    required this.postCount,
  });

  factory TagFilter.fromJson(Map<String, dynamic> json) => 
      _$TagFilterFromJson(json);
  Map<String, dynamic> toJson() => _$TagFilterToJson(this);
}

@JsonSerializable()
class AuthorFilter {
  final String username;
  @JsonKey(name: 'post_count')
  final int postCount;

  const AuthorFilter({
    required this.username,
    required this.postCount,
  });

  factory AuthorFilter.fromJson(Map<String, dynamic> json) => 
      _$AuthorFilterFromJson(json);
  Map<String, dynamic> toJson() => _$AuthorFilterToJson(this);
}