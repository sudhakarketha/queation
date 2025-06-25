#!/usr/bin/env python3
"""
Startup script for AI Question Answer Generator
Checks dependencies and provides helpful setup instructions
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_cors', 
        'openai', 'pymysql', 'python_dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} not found")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def check_node_installation():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found")
    print("Please install Node.js from https://nodejs.org/")
    return False

def check_mysql_connection():
    """Check if MySQL is accessible."""
    try:
        import pymysql
        # Try to connect with default settings
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Suman@123',
            database='questiondb',
            port=3306
        )
        connection.close()
        print("✅ MySQL connection successful")
        return True
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("Please ensure MySQL is running and database 'questiondb' exists")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=questiondb
DB_USER=root
DB_PASSWORD=Suman@123

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please update your OpenAI API key in the .env file")
    else:
        print("✅ .env file exists")

def install_frontend_dependencies():
    """Install frontend dependencies."""
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    node_modules = frontend_dir / 'node_modules'
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.check_call(['npm', 'install'], cwd=frontend_dir)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    else:
        print("✅ Frontend dependencies already installed")
    
    return True

def start_backend():
    """Start the Flask backend server."""
    print("\n🚀 Starting Flask backend...")
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Backend stopped")

def main():
    """Main startup function."""
    print("🤖 AI Question Answer Generator - Startup Check")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check Node.js
    if not check_node_installation():
        return
    
    # Check MySQL
    if not check_mysql_connection():
        print("\n💡 To fix MySQL issues:")
        print("1. Start MySQL server")
        print("2. Create database: CREATE DATABASE questiondb;")
        print("3. Or run: mysql -u root -p < init.sql")
        return
    
    # Create .env file
    create_env_file()
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        return
    
    print("\n✅ All checks passed!")
    print("\n🎯 Next steps:")
    print("1. Update your OpenAI API key in .env file")
    print("2. Start the backend: python app.py")
    print("3. Start the frontend: cd frontend && npm run dev")
    print("4. Open http://localhost:5173 in your browser")
    
    # Ask if user wants to start backend now
    response = input("\n🚀 Start backend server now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        start_backend()

if __name__ == '__main__':
    main() 