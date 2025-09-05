# Symfony 5 Project

![CI](https://github.com/napestershine/sf5/workflows/CI/badge.svg)

## Setup

### JWT Keys Generation
```sh
openssl genrsa -out config/jwt/private.pem -aes256 4096
openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem
```

### Create a user
```json
{
	"username": "admin",
    "name": "Manu",
    "email": "manu@blog.com",
    "password": "123"
}
```

### Create a blog post
```json

```