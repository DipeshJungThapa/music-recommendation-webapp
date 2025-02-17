const fs = require('fs');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');
const fileUpload = require('./file-upload');
const HttpError = require('./http-error');

const SPOTIFY_CLIENT_ID = process.env.SPOTIFY_CLIENT_ID;
const SPOTIFY_CLIENT_SECRET = process.env.SPOTIFY_CLIENT_SECRET;

const getSpotifyAccessToken = async () => {
  try {
    const response = await axios.post(
      'https://accounts.spotify.com/api/token',
      new URLSearchParams({ grant_type: 'client_credentials' }),
      {
        headers: {
          Authorization: `Basic ${Buffer.from(`${SPOTIFY_CLIENT_ID}:${SPOTIFY_CLIENT_SECRET}`).toString('base64')}`,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    return response.data.access_token;
  } catch (error) {
    console.error(
      'Error getting Spotify access token:',
      error.response?.data || error.message
    );
    throw new Error('Failed to get Spotify access token');
  }
};

const fetchTrackDetails = async (trackName, artistName) => {
  const token = await getSpotifyAccessToken();
  const searchQuery = encodeURIComponent(`${trackName} ${artistName}`);
  const searchUrl = `https://api.spotify.com/v1/search?q=${searchQuery}&type=track&limit=1`;

  try {
    const searchResponse = await axios.get(searchUrl, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const track = searchResponse.data.tracks.items[0];
    if (!track) {
      return null;
    }
    return {
      spotify_url: track.external_urls.spotify,
      album_cover: track.album.images.length ? track.album.images[0].url : null,
    };
  } catch (error) {
    console.error(
      'Error fetching track details from Spotify:',
      error.response?.data || error.message
    );
    throw new Error('Failed to fetch track details');
  }
};

const recommendation = async (req, res) => {
  const audioFile = req.file;
  if (!audioFile) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const filePath = path.join(__dirname, audioFile.path);

  const form = new FormData();
  form.append('file', fs.createReadStream(filePath), {
    filename: audioFile.originalname,
    contentType: audioFile.mimetype,
  });

  try {
    const response = await axios.post('http://localhost:7000/recommend', form, {
      headers: {
        ...form.getHeaders(),
      },
    });

    const recommendedTracks = response.data.recommended_tracks;
    const tracksWithMetadata = await Promise.all(
      recommendedTracks.map(async (track) => {
        const metadata = await fetchTrackDetails(track.track_name, track.artist);
        return { ...track, ...metadata };
      })
    );

    fs.unlink(filePath, (err) => {
      if (err) {
        if (err.code === 'ENOENT') {
          console.log('File not found, nothing to delete.');
        } else {
          console.error('Error deleting file:', err);
        }
      }
    });

    res.status(200).json({ recommended_tracks: tracksWithMetadata });
  } catch (error) {
    console.error(
      'Error sending file to recommendation service:',
      error.response?.data || error.message
    );

    fs.unlink(filePath, (err) => {
      if (err) {
        console.error('Error deleting file after failure:', err);
      }
    });

    res.status(500).json({ error: 'Failed to process the file' });
  }
};

module.exports = {
  recommendation,
  fileUpload,
};
