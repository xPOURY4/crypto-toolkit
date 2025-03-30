# 🔐 Comprehensive Guide to Crypto Toolkit

> [فارسی](READMEfa.md) | English

## 📋 Table of Contents
- [Introduction](#introduction)
- [Installation and Setup](#installation-and-setup)
- [Logging In](#logging-in)
- [User Panel](#user-panel)
- [Admin Panel](#admin-panel)
- [Features and Capabilities](#features-and-capabilities)
- [Step-by-Step Guide](#step-by-step-guide)
- [Real-World Applications](#real-world-applications)
- [Contributing](#contributing)
- [Copyright](#copyright)

## 🚀 Introduction

Crypto Toolkit is a comprehensive educational platform for learning about the world of cryptocurrencies and blockchain. This platform contains educational content in various categories, allowing users to read materials, bookmark them, and take advantage of its diverse features.

This project is designed to provide a reliable and practical educational resource for individuals interested in blockchain technology and cryptocurrencies. The educational content covers everything from basic concepts to advanced topics and is suitable for users with different levels of knowledge and experience.

## ⚙️ Installation and Setup

### Prerequisites
- Node.js version 14 or higher
- npm or yarn
- Python 3.9 or higher (for backend)

### Installation Steps

1. **Clone the Repository** 📂
   ```bash
   git clone https://github.com/xPOURY4/crypto-toolkit.git
   cd crypto-toolkit
   ```

2. **Install Frontend Dependencies** 🖥️
   ```bash
   cd frontend
   npm install
   ```

3. **Install Backend Dependencies** 🔧
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Start the Frontend Development Server** 🚀
   ```bash
   cd ../frontend
   npm run dev
   ```

5. **Start the Backend Development Server** 🏃
   ```bash
   cd ../backend
   python main.py
   ```

You can now access the application at `http://localhost:5173` (or the port shown in your terminal).

## 🔑 Logging In

To access all features of the platform, you need to log in to your account. For development and testing, you can use the following accounts:

### Admin Account
- **Email**: admin@example.com
- **Password**: admin

### Regular User Account
- **Email**: user@example.com
- **Password**: password

## 👤 User Panel

After logging in, users are directed to the dashboard which includes the following sections:

### Dashboard 📊
- Display a summary of bookmarked content
- Recently viewed content
- Personalized recommendations

### Categories 📁
- View all content categories
- Search within categories
- Filter by topic

### Educational Content 📚
- View educational content in each category
- Bookmark content for later reading
- Search and filter content

### Bookmarks 🔖
- View list of bookmarked content
- Remove content from bookmarks
- Sort by date added or name

### Notifications 🔔
- View system and content notifications
- Mark notifications as read
- Clear notifications

### Profile 👤
- Edit personal information
- Change password
- Manage account security settings

### Appearance Settings 🎨
- Toggle light/dark mode
- Select color theme (default, ocean, sunset, forest)
- Content display settings

## 👑 Admin Panel

The admin panel is only accessible to users with the `admin` role and includes the following sections:

### User Management 👥
- View user list
- Add, edit, and delete users
- Change user status (active/inactive)
- Change user roles (admin/regular user)

### Category Management 📋
- View category list
- Add, edit, and delete categories
- Change category status (active/inactive)

### Content Management 📝
- View list of educational content
- Add, edit, and delete content
- Change content status (published/draft/archived)
- Change content category
- Set content difficulty level

## ✨ Features and Capabilities

### Dark/Light Mode 🌓
The application supports dark and light modes. Users can:
- Manually switch between dark and light modes
- Set the application to follow system settings
- Adjust transition time between modes

### Color Themes 🎨
Four different color themes are available in the application:
- **Default**: Combination of teal and blue colors
- **Ocean**: Combination of dark and light blue colors 🌊
- **Sunset**: Combination of orange and red colors 🌅
- **Forest**: Combination of green and teal colors 🌲

### Security 🔒
- Authentication using JWT tokens
- WebAuthn support for passwordless authentication
- Access restrictions based on user role
- Password change and recovery options
- Advanced encryption for storing sensitive data

### Responsiveness 📱
All pages of the application are designed responsively and display correctly on different devices:
- Mobile phones (width less than 640px)
- Tablets (width between 640px and 1024px)
- Desktop (width greater than 1024px)

### Performance Optimization ⚡
- Lazy loading for components and images
- Data caching to reduce network requests
- Search Engine Optimization (SEO)

## 📝 Step-by-Step Guide

### 1. Logging in as a Regular User 👤
1. Go to the login page at `/login`
2. Enter the regular user email and password
3. Click the "Login" button
4. You'll be directed to the user dashboard

### 2. Logging in as an Admin 👑
1. Go to the login page at `/login`
2. Enter the admin email and password
3. Click the "Login" button
4. You'll be directed to the admin dashboard
5. To access management sections, select "User Management", "Category Management", or "Content Management" from the main menu

### 3. Browsing Categories and Content 🔍
1. Select "Categories" from the main menu
2. Click on a category of interest to view its content
3. Click on a content title to view its details
4. To bookmark content, click on the "Bookmark" icon

### 4. Managing Profile and Settings ⚙️
1. Click on your username at the top of the page
2. Select "Profile" from the dropdown menu
3. Edit your personal information
4. To change your password, fill in the appropriate fields
5. To change appearance settings, select "Appearance Settings" from the main menu

### 5. Adding New Content (Admin Only) ✏️
1. From the admin panel, select "Content Management"
2. Click the "Add Content" button
3. Fill out the form and select the appropriate category
4. Enter the educational content in the Markdown editor
5. Select the publication status (draft/published)
6. Click the "Save" button

## 🌐 Real-World Applications

### Blockchain Development Team Training 👨‍💻
The Crypto Toolkit platform is extremely useful for training new members of blockchain development teams. Managers can manage documentation and educational resources in a centralized location and track team members' progress.

### Introduction to Cryptocurrency Concepts 💰
For newcomers to the world of cryptocurrencies, this platform serves as a comprehensive educational resource. Users can start with basic concepts and gradually move on to more advanced topics.

### Security Reference for Developers 🛡️
Smart contract developers can use the security resources available on the platform to identify and prevent common vulnerabilities.

### Use in Educational Settings 🎓
Instructors and universities can use this platform to deliver courses on blockchain and cryptocurrencies.

## 🤝 Contributing

We welcome your contributions to the development of this project. To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ©️ Copyright

Copyright (c) 2025 xPOURY4

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
