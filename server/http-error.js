class HttpError extends Error {
  constructor(message, errcode) {
    super(message);
    if(typeof errcode!=='number'|| errcode<100 || errcode>599){
      throw new Error(`Invalid status code:${errcode}`);
    }
    this.code = errcode;
  }

}
module.exports = HttpError;
