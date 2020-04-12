```sh
openssl genrsa -out config/jwt/private.pem -aes256 4096
openssl rsa -pubout -in config/jwt/private.pem -out config/jwt/public.pem
```

### create a user
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