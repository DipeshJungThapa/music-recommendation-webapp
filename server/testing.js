// test-spotify.js
const axios = require('axios');
require('dotenv').config();

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
  }
};

// Test the fetchTrackDetails function
const trackName = 'Shape of You'; // Change this to any track you want to search
const artistName = 'Ed Sheeran'; // Change this to the corresponding artist

// Call the function to fetch track details
fetchTrackDetails(trackName, artistName)
  .then((details) => {
    if (details) {
      console.log('Track details:', details);
    } else {
      console.log('Track not found.');
    }
  })
  .catch((err) => console.error('Error:', err));
