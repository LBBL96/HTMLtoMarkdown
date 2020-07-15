class HTML:
    """
    Uses BeautifulSoup to parse tags. HTML Various methods can be called to return 
    text and images or to create a Markdown file.

    Args:
        url: A web URL, a file, or a string
        file: Default is False. Set to True if url is a file.
        text: Default is False. Set to True if url is a string.

    Returns:
        A Beautiful Soup object with methods to convert HTML to Markdown.

    Raises:
        ValueError: if Args are not properly inputted.  
    """
    
    def __init__(self, url, file=False, text=False):
        from bs4 import BeautifulSoup
        import requests
        self.url = url

        if not file and not text:
            response = requests.get(self.url)
        elif file and not text:
            with open(self.url) as file:
                response = file.read()
        elif text and not file:
            response = self.url
        else:
            raise ValueError("Input requires that at least one of `file` or `text` be False.")

        soup = BeautifulSoup(response.text, 'html.parser')


    def text_list(self, soup):
        """
        Returns:
            A list containing text contained within `p` tags. Each tag's text is a 
            separate entry.
        """
        return [tag.text for tag in soup.find_all('p')]

    def images(self, soup):
        """
        Returns:
            A list of all images in the document, regardless of their placement on the page.
        """
        return soup.find_all('img')

    def figures(self, soup):
        """
        Constrained to images within `figure` blocks. Useful in cases where the HTML contains 
        ads or other images that the user wishes to exclude. 

        Returns:
             None

        Methods:
            image_only: Returns a list of images within figure block.
            captions: Returns a list of captions of images within a figure block.
            img_dict: Returns a dictionary of tuples of images and their captions. Keys are
                sequential numbers.
            
        """
        images = []
        captions = []
        img_dict = {}

        for item in soup.find_all('figure'):
            for source in item.find_all('img'):
                try:
                    images.append(source['src'])
                    if item.text:
                        captions.append(item.text)
                    else:
                        captions.append(None)
                except:
                    pass

        def image_only():
            """
            Returns:
                List of images found within `figure` blocks.
            """
            return images
        
        def captions():
            """
            Returns:
                List of captions for each image found within `figure` blocks. If no
                caption exists for an image, None is appended to the list.
            """
            return captions

        def img_dict():
            """
            Returns:
                Dictionary of images and captions found within `figure` blocks. The keys are
                sequential numbers starting with 1 and the values are a tuple.
            """
            i = 0
            while i < len(images):
                img_dict[i + 1] = images[i], captions[i]
                i += 1

            return img_dict