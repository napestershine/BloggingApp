<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\BlogPost;
use App\Repository\BlogPostRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Serializer\SerializerInterface;

/**
 * Class BlogController
 * @package App\Controller
 *
 * @Route("/blog")
 */
class BlogController extends AbstractController
{
    /**
     * @Route("/{page}", name="blog_list", defaults={"page": 5}, requirements={"page"="\d+"})
     * @param Request $request
     * @param BlogPostRepository $blogPostRepository
     * @param int $page
     * @return JsonResponse
     */
    public function list(Request $request, BlogPostRepository $blogPostRepository, $page = 1)
    {
        $limit = $request->get('limit', 10);
        $blogPosts = $blogPostRepository->findAll();

        return new JsonResponse([
            'page' => $page,
            'limit' => $limit,
            'data' => \array_map(function (BlogPost $blogPost) {
                return $this->generateUrl('blog_by_slug', ['slug' => $blogPost->getSlug()]);
            }, $blogPosts)
        ]);
    }

    /**
     * @Route("/post/{id}", name="blog_by_id", requirements={"id"="\d+"}, methods={"GET"})
     * @param BlogPostRepository $blogPostRepository
     * @param $id
     * @return JsonResponse
     */
    public function post(BlogPostRepository $blogPostRepository, $id)
    {
        return $this->json($blogPostRepository->find($id));
    }

    /**
     * @Route("/post/{slug}", name="blog_by_slug", methods={"GET"})
     * @param BlogPostRepository $blogPostRepository
     * @param $slug
     * @return JsonResponse
     */
    public function postBySlug(BlogPostRepository $blogPostRepository, $slug)
    {
        return $this->json($blogPostRepository->findOneBy(['slug' => $slug]));
    }

    /**
     * @Route("/add", name="blog_add", methods={"POST"})
     *
     * @param Request $request
     * @param SerializerInterface $serializer
     * @param EntityManagerInterface $entityManager
     * @return JsonResponse
     */
    public function add(Request $request, SerializerInterface $serializer, EntityManagerInterface $entityManager)
    {
        $blogPost = $serializer->deserialize($request->getContent(), BlogPost::class, 'json');
        $entityManager->persist($blogPost);
        $entityManager->flush();

        return $this->json($blogPost);
    }

    /**
     * @Route("/post/{id}", name="blog_delete", methods={"DELETE"})
     * @param EntityManagerInterface $entityManager
     * @param $id
     * @return JsonResponse
     */
    public function delete(EntityManagerInterface $entityManager, $id)
    {
        $post = $entityManager->getRepository(BlogPost::class)->find($id);
        $entityManager->remove($post);
        $entityManager->flush();
        return $this->json(null, Response::HTTP_NO_CONTENT);
    }

}
