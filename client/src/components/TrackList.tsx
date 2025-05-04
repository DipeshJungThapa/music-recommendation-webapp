import React from 'react';
import TrackItem from './TrackItem';
import Card from './UI/Card';
import './TrackList.css';

type Track = {
  album_cover: string;
  track_name: string;
  artist: string;
  genre: string;
  spotify_url: string;
};

type TrackListProps = {
  tracks: Track[];
};

const TrackList: React.FC<TrackListProps> = ({ tracks }) => {
  if (tracks.length === 0) {
    return (
      <div className="track-list">
        <Card className="">
          <h2>No Tracks found. Try uploading a different file.</h2>
        </Card>
      </div>
    );
  }

  return (
    <div className="track-list">
      <ul>
        {tracks.map((track) => (
          <TrackItem
            key={track.track_name}
            album_cover={track.album_cover}
            track_name={track.track_name}
            artist={track.artist}
            genre={track.genre}
            spotify_url={track.spotify_url}
          />
        ))}
      </ul>
    </div>
  );
};
export default TrackList;
