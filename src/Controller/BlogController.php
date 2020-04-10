<?php

namespace App\Controller;

use App\Entity\BlogPost;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
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
     * @param int $page
     * @param Request $request
     * @return JsonResponse
     */
    public function list(Request $request, $page = 1)
    {
        return new JsonResponse([
            'page' => $page,
            'limit' => $request->get('limit')
        ]);
    }

    /**
     * @Route("/{id}", name="blog_by_id", requirements={"id"="\d+"}, methods={"GET"})
     */
    public function post($id)
    {
        return $this->json([]);
    }

    /**
     * @Route("/{slug}", name="blog_by_slug", methods={"GET"})
     */
    public function postBySlug($slug)
    {
        return $this->json([]);
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

}
