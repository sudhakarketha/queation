# 🤖 AI Question Answer Generator

A full-stack web application that allows users to upload questions with multiple choice answers and receive AI-generated correct answers with detailed explanations.

## 🚀 Features

- **Question Upload**: Upload questions with 4 multiple choice options
- **AI Analysis**: Get AI-generated correct answers with explanations
- **Fallback System**: Works even when OpenAI API is unavailable
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Question Management**: View, delete, and manage uploaded questions
- **Real-time Feedback**: Success/error messages with user-friendly notifications

## 🛠️ Tech Stack

### Backend
- **Python Flask**: RESTful API server
- **MySQL**: Database for storing questions and answers
- **OpenAI API**: AI-powered answer generation
- **SQLAlchemy**: Database ORM

### Frontend
- **React 19**: Modern UI framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **Axios**: HTTP client for API calls

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.8+** installed
2. **Node.js 16+** installed
3. **MySQL** server running
4. **OpenAI API Key** (optional, but recommended)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd questions

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Database Setup

1. **Start MySQL server**
2. **Create database**:
   ```sql
   CREATE DATABASE questiondb;
   ```
3. **Or run the provided SQL script**:
   ```bash
   mysql -u root -p < init.sql
   ```

### 3. Configuration

Create a `.env` file in the root directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=questiondb
DB_USER=root
DB_PASSWORD=your_password_here

# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 4. Run the Application

#### Start Backend (Terminal 1)
```bash
python app.py
```
The Flask API will start at `http://localhost:5000`

#### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
The React app will start at `http://localhost:5173`

### 5. Access the Application

Open your browser and navigate to `http://localhost:5173`

## 🔧 API Endpoints

### Health Check
- **GET** `/health` - Check API status

### Questions
- **GET** `/questions` - Get all questions
- **GET** `/questions/{id}` - Get specific question
- **POST** `/upload` - Upload new question
- **DELETE** `/questions/{id}` - Delete question

### Example API Usage

```bash
# Upload a question
curl -X POST http://localhost:5000/upload \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the capital of France?",
    "choices": ["London", "Paris", "Berlin", "Madrid"]
  }'

# Get all questions
curl http://localhost:5000/questions
```

## 🎯 How to Use

1. **Upload Questions**: Fill in the question text and 4 answer choices
2. **Generate Answers**: Click "Generate Answer" to get AI analysis
3. **View Results**: See the correct answer and detailed explanation
4. **Manage Questions**: View all uploaded questions in the history section
5. **Delete Questions**: Remove unwanted questions using the delete button

## 🔑 OpenAI API Setup

### Getting an API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key and add it to your `.env` file

### Handling API Quotas

If you encounter quota issues:
1. Check your usage at [OpenAI Usage](https://platform.openai.com/usage)
2. Add a payment method to your account
3. The application will automatically use fallback analysis if API is unavailable

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in `.env`
   - Verify database exists

2. **OpenAI API Errors**
   - Check API key is correct
   - Verify account has sufficient credits
   - Application will use fallback mode if API fails

3. **Frontend Not Loading**
   - Ensure backend is running on port 5000
   - Check CORS settings
   - Verify all dependencies are installed

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your `.env` file for detailed error messages.

## 📁 Project Structure

```
questions/
├── app.py                 # Flask main application
├── config.py             # Configuration settings
├── question_model.py     # Database models
├── requirements.txt      # Python dependencies
├── init.sql             # Database initialization
├── services/
│   └── ai_answer_generator.py  # AI answer generation logic
└── frontend/
    ├── src/
    │   ├── App.tsx       # Main React component
    │   ├── App.css       # Styles
    │   └── main.tsx      # React entry point
    ├── package.json      # Node dependencies
    └── vite.config.ts    # Vite configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section
2. Review the logs in the terminal
3. Ensure all dependencies are up to date
4. Create an issue with detailed error information

## 🎉 Features Roadmap

- [ ] User authentication
- [ ] Question categories/tags
- [ ] Export questions to PDF
- [ ] Bulk question upload
- [ ] Advanced AI models selection
- [ ] Question difficulty levels
- [ ] Performance analytics

---

**Happy Question Answering! 🎓** 