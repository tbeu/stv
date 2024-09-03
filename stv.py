import os

import pyrankvote
from pyrankvote import Candidate, Ballot


def get_all_files(directory):
    """Get a list of all CSV files in the given directory."""
    return [f for f in os.listdir(directory)]


def read_votes_from_csv(file_path):
    """Read votes from a CSV file where each line represents a single candidate."""
    votes = []
    with open(file_path) as file:
        for line in file:
            candidate_name = line.strip()
            if bool(candidate_name) and candidate_name not in votes:
                votes.append(candidate_name)
    return Ballot(ranked_candidates=[Candidate(candidate_name) for candidate_name in votes])


def run_stv(directory):
    """Run the Single Transferable Vote (STV) algorithm on all CSV files in the directory."""
    all_votes = []
    all_files = get_all_files(directory)
    
    # Collect votes from all CSV files
    for file in all_files:
        file_path = os.path.join(directory, file)
        vote = read_votes_from_csv(file_path)
        all_votes.append(vote)
    
    if bool(all_votes):
        # Get a unique list of candidates
        candidates = list({candidate for ballot in all_votes for candidate in ballot.ranked_candidates})

        # Run the STV election
        election_result = pyrankvote.instant_runoff_voting(candidates, all_votes)
        print(election_result)
    else:
        print("No votes found in the provided CSV files.")


# Replace with the directory containing your CSV files
module_dir = os.path.split(__file__)[0]
directory_path = os.path.join(module_dir, 'votes')
run_stv(directory_path)
