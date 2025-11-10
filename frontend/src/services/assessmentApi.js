import api from './api'

export const getAssessment = async (assessmentId) => {
  const response = await api.get(`/assessments/${assessmentId}`)
  return response.data
}

export const getAllAssessments = async () => {
  const response = await api.get('/assessments')
  return response.data
}

export const executeCode = async (code, language, input = null) => {
  const response = await api.post('/execute', {
    code,
    language,
    input,
  })
  return response.data
}

export const executeWithTests = async (
  code,
  language,
  questionId,
  assessmentId,
  candidateId = 'anonymous',
  includeHidden = false
) => {
  const response = await api.post('/execute/test', {
    code,
    language,
    question_id: questionId,
    assessment_id: assessmentId,
    candidate_id: candidateId,
    include_hidden: includeHidden,
  })
  return response.data
}

export const getSubmissions = async (assessmentId, questionId, candidateId) => {
  const response = await api.get('/execute/submissions', {
    params: {
      assessment_id: assessmentId,
      question_id: questionId,
      candidate_id: candidateId,
    },
  })
  return response.data
}

