import 'package:flutter/material.dart';
import '../models/blog_post.dart';

class BlogPostCard extends StatelessWidget {
  final BlogPost blogPost;
  final VoidCallback? onTap;
  final bool isCompact;

  const BlogPostCard({
    super.key,
    required this.blogPost,
    this.onTap,
    this.isCompact = false,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: isCompact ? EdgeInsets.zero : const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: EdgeInsets.all(isCompact ? 12 : 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                blogPost.title,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.bold,
                  fontSize: isCompact ? 18 : null,
                ),
                maxLines: isCompact ? 1 : 2,
                overflow: TextOverflow.ellipsis,
              ),
              SizedBox(height: isCompact ? 6 : 8),
              
              if (blogPost.publishedDate != null && !isCompact) ...[
                Row(
                  children: [
                    Icon(
                      Icons.schedule,
                      size: 16,
                      color: Theme.of(context).textTheme.bodySmall?.color,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      _formatDate(blogPost.publishedDate!),
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ],
                ),
                const SizedBox(height: 8),
              ],
              
              if (blogPost.author != null) ...[
                Row(
                  children: [
                    Icon(
                      Icons.person,
                      size: 14,
                      color: Theme.of(context).textTheme.bodySmall?.color,
                    ),
                    const SizedBox(width: 4),
                    Expanded(
                      child: Text(
                        'By ${blogPost.author!.name}',
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          fontSize: isCompact ? 11 : null,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
                SizedBox(height: isCompact ? 6 : 8),
              ],
              
              if (!isCompact) ...[
                Text(
                  blogPost.content,
                  style: Theme.of(context).textTheme.bodyMedium,
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 12),
              ],
              
              if (isCompact) Expanded(child: Container()),
              
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  if (blogPost.comments?.isNotEmpty == true)
                    Row(
                      children: [
                        Icon(
                          Icons.comment_outlined,
                          size: isCompact ? 14 : 16,
                          color: Theme.of(context).textTheme.bodySmall?.color,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          '${blogPost.comments!.length}',
                          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            fontSize: isCompact ? 11 : null,
                          ),
                        ),
                      ],
                    )
                  else
                    Icon(
                      Icons.comment_outlined,
                      size: isCompact ? 14 : 16,
                      color: Theme.of(context).textTheme.bodySmall?.color?.withOpacity(0.5),
                    ),
                  
                  if (isCompact && blogPost.publishedDate != null)
                    Text(
                      _formatDate(blogPost.publishedDate!),
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        fontSize: 10,
                      ),
                    )
                  else
                    Icon(
                      Icons.arrow_forward_ios,
                      size: isCompact ? 14 : 16,
                      color: Theme.of(context).textTheme.bodySmall?.color,
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.inDays > 7) {
      return '${date.day}/${date.month}/${date.year}';
    } else if (difference.inDays > 0) {
      return '${difference.inDays} day${difference.inDays == 1 ? '' : 's'} ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} hour${difference.inHours == 1 ? '' : 's'} ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} minute${difference.inMinutes == 1 ? '' : 's'} ago';
    } else {
      return 'Just now';
    }
  }
}