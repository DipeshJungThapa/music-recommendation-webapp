import React from 'react';

export type TrackProps = {
  album_cover: string;
  track_name: string;
  artist: string;
  genre: string;
  spotify_url: string;
};

const TrackItem: React.FC<TrackProps> = (props) => {
  return (
    <li className="track-item">
      <img
        src={props.album_cover}
        alt={props.track_name}
        className="album-cover"
      />
      <div className="track-info">
        <p>
          <strong>Track:</strong> {props.track_name}
        </p>
        <p>
          <strong>Artist:</strong> {props.artist}
        </p>
        <p>
          <strong>Genre:</strong> {props.genre}
        </p>
        <a
          href={props.spotify_url}
          target="_blank"
          rel="noopener noreferrer"
          className="spotify-link"
        >
          Listen on Spotify
        </a>
      </div>
    </li>
  );
};

export default TrackItem;
