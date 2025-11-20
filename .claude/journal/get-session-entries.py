#!/usr/bin/env python3
"""
Get all journal entries for today's sessions
Uses smart session detection with 5am cutoff for late-night sessions
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta

def get_todays_sessions():
    """
    Get all sessions that belong to today, using 5am cutoff for late-night sessions.

    Logic:
    - Group all entries by session_id
    - For each session, get first timestamp (when session started)
    - If session started before 5am, it belongs to previous day
    - Otherwise it belongs to the day it started
    - Return all entries for sessions that belong to today
    """
    db_path = Path(__file__).parent / 'journal.db'

    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # Determine "today" with 5am cutoff
    now = datetime.now()
    if now.hour < 5:  # Before 5am - we're still in "yesterday"
        today = (now - timedelta(days=1)).date()
    else:
        today = now.date()

    # Get first timestamp for each session (when it started)
    cursor = conn.execute(
        "SELECT session_id, MIN(timestamp) as start_time FROM journal GROUP BY session_id"
    )
    sessions = cursor.fetchall()

    # Determine which sessions belong to today
    today_session_ids = []
    for session in sessions:
        start_time = datetime.fromisoformat(session['start_time'])

        # If session started before 5am, it belongs to previous day
        if start_time.hour < 5:
            session_date = (start_time - timedelta(days=1)).date()
        else:
            session_date = start_time.date()

        if session_date == today:
            today_session_ids.append(session['session_id'])

    # Get all entries for today's sessions
    if not today_session_ids:
        conn.close()
        return []

    placeholders = ','.join('?' * len(today_session_ids))
    cursor = conn.execute(
        f"SELECT * FROM journal WHERE session_id IN ({placeholders}) ORDER BY timestamp ASC",
        today_session_ids
    )
    entries = cursor.fetchall()
    conn.close()

    return [dict(entry) for entry in entries]

def get_session_time_range():
    """
    Get earliest and latest timestamps from ALL of today's sessions combined.
    Returns tuple (earliest, latest) for use with git log.
    This gives the exact time range when work was actually being done.
    """
    db_path = Path(__file__).parent / 'journal.db'

    if not db_path.exists():
        return None, None

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # Determine "today" with 5am cutoff
    now = datetime.now()
    if now.hour < 5:
        today = (now - timedelta(days=1)).date()
    else:
        today = now.date()

    # Get first timestamp for each session
    cursor = conn.execute(
        "SELECT session_id, MIN(timestamp) as start_time FROM journal GROUP BY session_id"
    )
    sessions = cursor.fetchall()

    # Find today's session IDs
    today_session_ids = []
    for session in sessions:
        start_time = datetime.fromisoformat(session['start_time'])
        if start_time.hour < 5:
            session_date = (start_time - timedelta(days=1)).date()
        else:
            session_date = start_time.date()

        if session_date == today:
            today_session_ids.append(session['session_id'])

    if not today_session_ids:
        conn.close()
        return None, None

    # Get MIN and MAX timestamps across ALL of today's sessions
    placeholders = ','.join('?' * len(today_session_ids))
    cursor = conn.execute(
        f"SELECT MIN(timestamp) as earliest, MAX(timestamp) as latest FROM journal WHERE session_id IN ({placeholders})",
        today_session_ids
    )
    result = cursor.fetchone()
    conn.close()

    if result and result['earliest'] and result['latest']:
        earliest = datetime.fromisoformat(result['earliest'])
        latest = datetime.fromisoformat(result['latest'])
        return earliest, latest

    return None, None

def main():
    entries = get_todays_sessions()

    if not entries:
        print("No sessions found for today")
        return

    # Get time range for git log
    earliest, latest = get_session_time_range()
    if earliest and latest:
        print(f"Session time range: {earliest.strftime('%Y-%m-%d %H:%M')} to {latest.strftime('%Y-%m-%d %H:%M')}")
        print(f"Git log suggestion: git log --since=\"{earliest.strftime('%Y-%m-%d %H:%M:%S')}\" --until=\"{latest.strftime('%Y-%m-%d %H:%M:%S')}\" --pretty=format:\"%h - %s%n%b\" --stat")
        print()

    # Group by session for readability
    sessions = {}
    for entry in entries:
        sid = entry['session_id']
        if sid not in sessions:
            sessions[sid] = []
        sessions[sid].append(entry)

    print(f"Total interactions (today): {len(entries)}")
    print(f"Sessions: {len(sessions)}\n")
    print("="*80)

    current_session = None
    interaction_num = 0

    for entry in entries:
        # Show session boundary when switching sessions
        if entry['session_id'] != current_session:
            current_session = entry['session_id']
            print(f"\n{'='*80}")
            print(f"SESSION: {current_session}")
            print(f"{'='*80}")

        interaction_num += 1
        print(f"\n[{interaction_num}] {entry['timestamp']}")
        print(f"User: {entry['user_prompt']}")
        if entry['summary'] and entry['summary'] != 'No response recorded':
            print(f"Summary: {entry['summary']}")
        if entry['tools_used']:
            try:
                tools = json.loads(entry['tools_used'])
                if tools:
                    print(f"Tools: {', '.join(tools)}")
            except:
                pass
        print("-"*80)

if __name__ == '__main__':
    main()
