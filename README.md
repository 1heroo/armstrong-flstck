# Overview

This is a Django-based web application for a ceiling solutions company in Kyrgyzstan. The application serves as a business website showcasing various ceiling products, providing cost calculations, and handling customer inquiries. It features a product catalog with detailed specifications, an interactive cost calculator, and a contact form system for lead generation.

# User Preferences

Preferred communication style: Simple, everyday language.
Design preferences: Elegant monochromatic design with 80% white background, dark text/headers, and orange accents only on button hover effects.
Language support: Russian, Kyrgyz, and English multilingual interface.

# System Architecture

## Frontend Architecture
- **Template Engine**: Django's built-in template system with HTML templates extending a base layout
- **UI Framework**: Bootstrap 5 for responsive design and component styling
- **JavaScript**: Vanilla JavaScript for interactive features like the cost calculator and form validation
- **CSS**: Custom CSS with CSS variables for consistent theming and styling
- **Static Assets**: Organized in `/static/` directory with separate folders for CSS, JavaScript, and images

## Backend Architecture
- **Framework**: Django 4.2+ web framework following MVC pattern
- **Application Structure**: Single Django app called `main` handling all business logic
- **URL Routing**: Centralized URL configuration with app-level routing
- **Views**: Function-based views handling product display, cost calculation, and contact forms
- **Models**: Two main models - `Product` for ceiling product data and `ContactInquiry` for customer inquiries

## Data Models
- **Product Model**: Stores ceiling product information including name, description, pricing, category, weight specifications, and image URLs
- **ContactInquiry Model**: Captures customer contact information and messages with timestamps
- **Admin Interface**: Django admin integration for content management

## Form Handling
- **Django Forms**: Model-based forms for contact inquiries and calculation inputs
- **AJAX Support**: Real-time cost calculations without page refresh
- **Validation**: Server-side form validation with client-side enhancements

## Business Logic
- **Cost Calculator**: Real-time calculation based on room dimensions and selected ceiling type
- **Product Categorization**: Multiple ceiling categories (acoustic, decorative, metal, tiles, mineral fiber)
- **Responsive Design**: Mobile-first approach with Bootstrap responsive grid system
- **Internationalization**: Full multilingual support for English, Russian, and Kyrgyz languages
- **Bold Modern Design**: Metallic gray color scheme with rich orange gradients transitioning to dark tones

# External Dependencies

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for UI enhancement
- **CDN Delivery**: External CSS and JavaScript libraries loaded via CDN

## Django Framework
- **Django 4.2+**: Main web framework
- **Django Admin**: Built-in admin interface for content management
- **Django Forms**: Form handling and validation system
- **Django Templates**: Server-side template rendering

## Static Asset Management
- **Django Static Files**: Built-in static file handling system
- **Image Hosting**: External image URLs for product photos (currently using placeholder services)

## Development Environment
- **Python**: Core programming language
- **WSGI**: Web server gateway interface for deployment
- **Environment Variables**: Configuration management for sensitive settings like SECRET_KEY

## Potential Database
- **Default**: SQLite (Django default for development)
- **Production Ready**: Configurable for PostgreSQL or other databases
- **ORM**: Django's built-in Object-Relational Mapping system