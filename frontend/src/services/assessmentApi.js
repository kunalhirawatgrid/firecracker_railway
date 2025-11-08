/**
 * Assessment API client.
 */
import api from './api';

export const assessmentApi = {
  /**
   * Create a new assessment.
   */
  createAssessment: (data) => api.post('/assessments', data),

  /**
   * Get assessment by ID.
   */
  getAssessment: (assessmentId, candidateId) =>
    api.get(`/assessments/${assessmentId}?candidate_id=${candidateId}`),

  /**
   * Start an assessment.
   */
  startAssessment: (assessmentId, candidateId) =>
    api.post(`/assessments/${assessmentId}/start`, { candidate_id: candidateId }),

  /**
   * Get questions for an assessment.
   */
  getQuestions: (assessmentId, candidateId) =>
    api.get(`/assessments/${assessmentId}/questions?candidate_id=${candidateId}`),

  /**
   * Submit a solution.
   */
  submitSolution: (assessmentId, questionId, candidateId, data) =>
    api.post(`/assessments/${assessmentId}/questions/${questionId}/submit?candidate_id=${candidateId}`, data),

  /**
   * Execute code (for testing).
   */
  executeCode: (data) => api.post('/execute/run', data),
};

