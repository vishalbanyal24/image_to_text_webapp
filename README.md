# Image to Text Generator - Black & White Webapp

A clean, modern, and minimalist web application for converting images to text descriptions. Built with Django and featuring a sophisticated black and white design aesthetic.

## Features

- **Clean Black & White Design**: Modern monochrome interface with elegant typography
- **Multiple Input Methods**: Upload files, paste URLs, or specify local paths
- **Drag & Drop Support**: Intuitive file handling with visual feedback
- **Real-time Preview**: See your images before processing
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Accessibility Focused**: Built with ARIA labels and keyboard navigation
- **Paste Support**: Paste images directly from clipboard

## Design Philosophy

This webapp embraces the power of simplicity through:
- **Monochrome Color Scheme**: Pure black (#000000) and white (#ffffff) with subtle grays
- **Clean Typography**: Inter font family for excellent readability
- **Minimalist UI**: Focused on content and functionality
- **Smooth Animations**: Subtle hover effects and transitions
- **High Contrast**: Excellent accessibility and visual clarity

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with modern design principles
- **Fonts**: Inter (Google Fonts)
- **Icons**: SVG icons for crisp display at any size

## Getting Started

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

4. **Open Browser**: Navigate to `http://localhost:8000`

### Production Deployment

This project is configured for deployment on Railway. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy to Railway:**
1. Push your code to GitHub
2. Connect your repository to Railway
3. Set environment variables (SECRET_KEY, GOOGLE_API_KEY, etc.)
4. Deploy automatically

## Usage

1. **Choose Input Method**: Select from Upload, URL, or Local Path tabs
2. **Add Image**: Drag & drop, browse files, or paste from clipboard
3. **Generate**: Click "Generate Description" to process your image
4. **View Results**: See the AI-generated description in the chat interface

## File Structure

```
project1/
├── image_converter/          # Django app
│   ├── models.py            # Data models
│   ├── views.py             # View logic
│   ├── urls.py              # URL routing
│   └── admin.py             # Admin interface
├── static/
│   ├── css/
│   │   └── style.css        # Black & white styling
│   └── js/
│       └── app.js           # Interactive functionality
├── templates/
│   └── image_converter/
│       └── index.html       # Main interface
├── Procfile                 # Railway deployment configuration
├── runtime.txt              # Python version specification
├── railway.json             # Railway-specific settings
├── build.sh                 # Build script for deployment
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
├── DEPLOYMENT.md           # Deployment guide
└── manage.py               # Django management
```

## Customization

The black and white theme can be easily customized by modifying:
- **Colors**: Update CSS custom properties in `style.css`
- **Typography**: Modify font families and sizes
- **Spacing**: Adjust padding, margins, and border radius values
- **Animations**: Customize transition timings and effects

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please ensure all changes maintain the black and white aesthetic and accessibility standards.
