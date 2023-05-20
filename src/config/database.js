const mongodb_uri = process.env.MONGODB_URI;

module.exports = {
    remoteUrl : mongodb_uri,
    localUrl: mongodb_uri
};
