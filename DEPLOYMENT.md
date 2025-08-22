# Railway Deployment Guide

This guide will help you deploy your Image to Text Generator Django application to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Git Repository**: Your project should be in a Git repository (GitHub, GitLab, etc.)
3. **Google AI API Key**: You'll need a Google AI API key for the image processing functionality

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository contains all the necessary files:
- `Procfile` - Tells Railway how to run your app
- `requirements.txt` - Lists all Python dependencies
- `runtime.txt` - Specifies Python version
- `railway.json` - Railway-specific configuration
- `build.sh` - Build script (optional)

### 2. Connect to Railway

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect it's a Python/Django project

### 3. Configure Environment Variables

In your Railway project dashboard, go to the "Variables" tab and add these environment variables:

```
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app
GOOGLE_API_KEY=your-google-ai-api-key
```

**Generate a secure SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(50))
```

### 4. Deploy

1. Railway will automatically start the deployment process
2. The build process will:
   - Install dependencies from `requirements.txt`
   - Run database migrations
   - Collect static files
   - Start the application with Gunicorn

### 5. Verify Deployment

1. Check the deployment logs in Railway dashboard
2. Visit your app URL: `https://your-app-name.railway.app`
3. Test the health endpoint: `https://your-app-name.railway.app/health/`

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | Development key |
| `DEBUG` | Debug mode | No | True |
| `ALLOWED_HOSTS` | Allowed hosts | No | localhost,127.0.0.1,.railway.app |
| `GOOGLE_API_KEY` | Google AI API key | Yes | None |

## Troubleshooting

### Common Issues

1. **Build Fails**: Check the build logs for missing dependencies
2. **Static Files Not Loading**: Ensure `whitenoise` is in requirements.txt
3. **Database Errors**: Make sure migrations are running properly
4. **API Key Issues**: Verify your Google AI API key is set correctly

### Logs

- View deployment logs in Railway dashboard
- Check application logs for runtime errors
- Monitor the health endpoint for application status

## Performance Optimization

1. **Static Files**: WhiteNoise handles static file serving efficiently
2. **Database**: Consider using PostgreSQL for production (Railway supports it)
3. **Caching**: Add Redis for caching if needed
4. **CDN**: Railway provides global CDN for static assets

## Security Considerations

1. **SECRET_KEY**: Always use a secure, unique secret key in production
2. **DEBUG**: Set to False in production
3. **ALLOWED_HOSTS**: Only include necessary domains
4. **HTTPS**: Railway provides automatic HTTPS
5. **API Keys**: Store sensitive keys as environment variables

## Monitoring

- Railway provides built-in monitoring and logging
- Set up alerts for application errors
- Monitor resource usage (CPU, memory, disk)
- Track response times and error rates

## Scaling

Railway automatically scales your application based on traffic. You can also:
- Set minimum and maximum instances
- Configure auto-scaling rules
- Monitor resource usage and costs

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Django Deployment Guide: [docs.djangoproject.com](https://docs.djangoproject.com/en/stable/howto/deployment/)
- Project Issues: Check the GitHub repository issues
