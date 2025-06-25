// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.tsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App








// import React, { useState, useEffect, FormEvent } from 'react';
// import axios, { AxiosError } from 'axios';
import React, { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import axios, { AxiosError } from 'axios';
import './App.css';

interface Question {
  id: number;
  question: string;
  choices: string[];
  answer: string;
  explanation: string;
  user_correction?: string | null;
}

interface ApiResponse {
  message: string;
  result: {
    answer: string;
    explanation: string;
    source: string;
    fact_checked?: boolean;
  };
  question_id: number;
}

interface ErrorResponse {
  error: string;
  details?: string;
}

function App() {
  const [question, setQuestion] = useState('');
  const [choices, setChoices] = useState(['', '', '', '']);
  const [questionsList, setQuestionsList] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [reportModal, setReportModal] = useState<{ open: boolean; qid: number | null }>({ open: false, qid: null });
  const [correction, setCorrection] = useState<string>('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await axios.post<ApiResponse>('http://localhost:5000/upload', {
        question,
        choices,
      });

      setSuccess(`Question saved successfully! Answer: ${response.data.result.answer}`);
      setQuestion('');
      setChoices(['', '', '', '']);
      fetchQuestions();
    } catch (error) {
      const err = error as AxiosError<ErrorResponse>;
      const errorMessage = err.response?.data?.error || err.message || 'Unknown error occurred';
      setError(`Error saving question: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchQuestions = async () => {
    try {
      const response = await axios.get<Question[]>('http://localhost:5000/questions');
      setQuestionsList(response.data);
    } catch (error) {
      const err = error as AxiosError;
      console.error('Error fetching questions:', err);
    }
  };

  const deleteQuestion = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this question?')) {
      return;
    }

    try {
      await axios.delete(`http://localhost:5000/questions/${id}`);
      setSuccess('Question deleted successfully!');
      fetchQuestions();
    } catch (error) {
      const err = error as AxiosError;
      setError(`Error deleting question: ${err.message}`);
    }
  };

  // Report/Correct Answer Modal Handlers
  const openReportModal = (qid: number) => {
    setReportModal({ open: true, qid });
    setCorrection('');
  };
  const closeReportModal = () => {
    setReportModal({ open: false, qid: null });
    setCorrection('');
  };
  const submitCorrection = async () => {
    if (!reportModal.qid || !['A', 'B', 'C', 'D'].includes(correction)) {
      setError('Please select a valid correction (A, B, C, or D).');
      return;
    }
    try {
      await axios.post(`http://localhost:5000/questions/${reportModal.qid}/report`, {
        correction,
      });
      setSuccess('Correction submitted!');
      closeReportModal();
      fetchQuestions();
    } catch (error) {
      const err = error as AxiosError<ErrorResponse>;
      setError(`Error submitting correction: ${err.response?.data?.error || err.message}`);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const clearMessages = () => {
    setError('');
    setSuccess('');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 AI Question Answer Generator</h1>
        <p>Upload questions with multiple choice answers and get AI-generated explanations</p>
      </header>

      <main className="app-main">
        {/* Upload Section */}
        <section className="upload-section">
          <h2>📝 Upload New Question</h2>
          <form onSubmit={handleSubmit} className="question-form">
            <div className="form-group">
              <label htmlFor="question">Question:</label>
              <textarea
                id="question"
                placeholder="Enter your question here..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                required
                rows={4}
              />
            </div>

            <div className="choices-group">
              <label>Answer Choices:</label>
              {choices.map((choice, index) => (
                <div key={index} className="choice-input">
                  <span className="choice-label">{String.fromCharCode(65 + index)}.</span>
                  <input
                    type="text"
                    placeholder={`Choice ${String.fromCharCode(65 + index)}`}
                    value={choice}
                    onChange={(e) => {
                      const newChoices = [...choices];
                      newChoices[index] = e.target.value;
                      setChoices(newChoices);
                    }}
                    required
                  />
                </div>
              ))}
            </div>

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? '🔄 Processing...' : '🚀 Generate Answer'}
            </button>
          </form>
        </section>

        {/* Messages */}
        {(error || success) && (
          <div className="messages">
            {error && (
              <div className="error-message" onClick={clearMessages}>
                ❌ {error}
              </div>
            )}
            {success && (
              <div className="success-message" onClick={clearMessages}>
                ✅ {success}
              </div>
            )}
          </div>
        )}

        {/* Questions List */}
        <section className="questions-section">
          <h2>📋 Questions History</h2>
          {questionsList.length === 0 ? (
            <div className="no-questions">
              <p>No questions uploaded yet. Start by uploading your first question!</p>
            </div>
          ) : (
            <div className="questions-grid">
              {questionsList.map((q) => {
                const userCorrectionIndex = q.user_correction ? ['A', 'B', 'C', 'D'].indexOf(q.user_correction) : -1;
                return (
                  <div key={q.id} className="question-card">
                    <div className="question-header">
                      <h3>Question #{q.id}</h3>
                      <button
                        onClick={() => deleteQuestion(q.id)}
                        className="delete-btn"
                        title="Delete question"
                      >
                        🗑️
                      </button>
                    </div>
                    <div className="question-content">
                      <p className="question-text">{q.question}</p>
                      <div className="choices-list">
                        {q.choices.map((choice, index) => {
                          const letter = String.fromCharCode(65 + index);
                          const isAICorrect = letter === q.answer;
                          const isUserCorrect = userCorrectionIndex === index;
                          return (
                            <div
                              key={index}
                              className={`choice-item ${isAICorrect ? 'correct' : ''} ${isUserCorrect ? 'user-correct' : ''}`}
                            >
                              <span className="choice-letter">{letter}</span>
                              <span className="choice-text">{choice}</span>
                              {isAICorrect && <span className="correct-badge">AI ✓</span>}
                              {isUserCorrect && <span className="user-correct-badge">User ✓</span>}
                            </div>
                          );
                        })}
                      </div>
                      <div className="answer-section">
                        <h4>AI Answer: {q.answer}</h4>
                        <div className="explanation">
                          <strong>Explanation:</strong>
                          <p>{q.explanation}</p>
                        </div>
                        {q.user_correction && (
                          <div className="user-correction-info">
                            <strong>User Correction:</strong> {q.user_correction}
                          </div>
                        )}
                        <button
                          className="report-btn"
                          onClick={() => openReportModal(q.id)}
                        >
                          Report/Correct Answer
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </main>

      {/* Report/Correct Modal */}
      {reportModal.open && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Report/Correct Answer</h3>
            <p>Select the correct answer (A, B, C, or D):</p>
            <div className="modal-choices">
              {['A', 'B', 'C', 'D'].map((letter) => (
                <button
                  key={letter}
                  className={`modal-choice-btn${correction === letter ? ' selected' : ''}`}
                  onClick={() => setCorrection(letter)}
                >
                  {letter}
                </button>
              ))}
            </div>
            <div className="modal-actions">
              <button onClick={submitCorrection} className="submit-btn">Submit Correction</button>
              <button onClick={closeReportModal} className="delete-btn">Cancel</button>
            </div>
          </div>
        </div>
      )}

      <footer className="app-footer">
        <p>© 2024 AI Question Answer Generator | Built with React + Flask + MySQL</p>
      </footer>
    </div>
  );
}

export default App;


