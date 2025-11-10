import json
import os
from typing import Dict, List, Optional
from pathlib import Path
from app.models.assessment import Assessment, Submission
from app.core.config import settings


class JSONStorage:
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path or settings.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.assessments_file = self.storage_path / "assessments.json"
        self.submissions_file = self.storage_path / "submissions.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create JSON files if they don't exist"""
        if not self.assessments_file.exists():
            self.assessments_file.write_text(json.dumps([], indent=2))
        if not self.submissions_file.exists():
            self.submissions_file.write_text(json.dumps([], indent=2))
    
    def _read_json(self, file_path: Path) -> List[Dict]:
        """Read and parse JSON file"""
        try:
            content = file_path.read_text()
            return json.loads(content) if content.strip() else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json(self, file_path: Path, data: List[Dict]):
        """Write data to JSON file"""
        file_path.write_text(json.dumps(data, indent=2, default=str))
    
    # Assessment methods
    def get_assessment(self, assessment_id: str) -> Optional[Assessment]:
        """Get assessment by ID"""
        assessments = self._read_json(self.assessments_file)
        for assessment_data in assessments:
            if assessment_data.get("id") == assessment_id:
                return Assessment.from_dict(assessment_data)
        return None
    
    def get_all_assessments(self) -> List[Assessment]:
        """Get all assessments"""
        assessments = self._read_json(self.assessments_file)
        return [Assessment.from_dict(a) for a in assessments]
    
    def create_assessment(self, assessment: Assessment) -> Assessment:
        """Create a new assessment"""
        assessments = self._read_json(self.assessments_file)
        assessments.append(assessment.to_dict())
        self._write_json(self.assessments_file, assessments)
        return assessment
    
    def update_assessment(self, assessment: Assessment) -> Optional[Assessment]:
        """Update an existing assessment"""
        assessments = self._read_json(self.assessments_file)
        for i, assessment_data in enumerate(assessments):
            if assessment_data.get("id") == assessment.id:
                assessments[i] = assessment.to_dict()
                self._write_json(self.assessments_file, assessments)
                return assessment
        return None
    
    # Submission methods
    def create_submission(self, submission: Submission) -> Submission:
        """Create a new submission"""
        submissions = self._read_json(self.submissions_file)
        submissions.append(submission.to_dict())
        self._write_json(self.submissions_file, submissions)
        return submission
    
    def get_submissions(
        self,
        assessment_id: Optional[str] = None,
        question_id: Optional[str] = None,
        candidate_id: Optional[str] = None,
    ) -> List[Submission]:
        """Get submissions with optional filters"""
        submissions_data = self._read_json(self.submissions_file)
        submissions = [Submission.from_dict(s) for s in submissions_data]
        
        if assessment_id:
            submissions = [s for s in submissions if s.assessment_id == assessment_id]
        if question_id:
            submissions = [s for s in submissions if s.question_id == question_id]
        if candidate_id:
            submissions = [s for s in submissions if s.candidate_id == candidate_id]
        
        return submissions


# Global storage instance
storage = JSONStorage()

