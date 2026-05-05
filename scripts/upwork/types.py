"""Upwork data type definitions."""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class JobListing:
    title: str = ""
    url: str = ""
    uid: str = ""
    posted_date: str = ""
    budget: str = ""
    job_type: str = ""      # hourly | fixed
    description: str = ""
    skills: list[str] = field(default_factory=list)
    payment_verified: bool = False
    client_country: str = ""
    proposals_count: str = ""

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "uid": self.uid,
            "postedDate": self.posted_date,
            "budget": self.budget,
            "jobType": self.job_type,
            "description": self.description,
            "skills": self.skills,
            "paymentVerified": self.payment_verified,
            "clientCountry": self.client_country,
            "proposalsCount": self.proposals_count,
        }


@dataclass
class JobDetail(JobListing):
    full_description: str = ""
    experience_level: str = ""
    project_duration: str = ""
    weekly_hours: str = ""
    client_rating: str = ""
    client_total_spent: str = ""
    apply_url: str = ""

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "fullDescription": self.full_description,
            "experienceLevel": self.experience_level,
            "projectDuration": self.project_duration,
            "weeklyHours": self.weekly_hours,
            "clientRating": self.client_rating,
            "clientTotalSpent": self.client_total_spent,
            "applyUrl": self.apply_url,
        })
        return d


@dataclass
class ProposalResult:
    job_url: str = ""
    job_title: str = ""
    success: bool = False
    message: str = ""
    proposal_url: str = ""

    def to_dict(self) -> dict:
        return {
            "jobUrl": self.job_url,
            "jobTitle": self.job_title,
            "success": self.success,
            "message": self.message,
            "proposalUrl": self.proposal_url,
        }


@dataclass
class MyProposal:
    job_title: str = ""
    job_url: str = ""
    status: str = ""
    submitted_date: str = ""
    bid: str = ""

    def to_dict(self) -> dict:
        return {
            "jobTitle": self.job_title,
            "jobUrl": self.job_url,
            "status": self.status,
            "submittedDate": self.submitted_date,
            "bid": self.bid,
        }
