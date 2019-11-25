import torch
from torch.autograd import Variable
import shop_recognizer.scene_text_recognizer.moran.tools.utils as utils
import shop_recognizer.scene_text_recognizer.moran.tools.dataset as dataset
from PIL import Image
from collections import OrderedDict
from shop_recognizer.scene_text_recognizer.moran.core.moran import MORAN


class TextRecognizer:

    def __init__(self):
        self.model_path = 'shop_recognizer/scene_text_recognizer/moran/model/blstm.pth'
        self.alphabet = '0:1:2:3:4:5:6:7:8:9:a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z:$'
        self.cuda_flag = False
        self.recognizer = None
        if torch.cuda.is_available():
            self.cuda_flag = True
            self.recognizer = MORAN(1, len(self.alphabet.split(':')), 256, 32, 100, BidirDecoder=True, CUDA=self.cuda_flag)
            self.recognizer = self.recognizer.cuda()
        else:
            self.recognizer = MORAN(1, len(self.alphabet.split(':')), 256, 32, 100, BidirDecoder=True,
                          inputDataType='torch.FloatTensor',
                          CUDA=self.cuda_flag)

        print('loading pretrained model from %s' % self.model_path)
        if self.cuda_flag:
            self.state_dict = torch.load(self.model_path)
        else:
            self.state_dict = torch.load(self.model_path, map_location='cpu')

        MORAN_state_dict_rename = OrderedDict()
        for k, v in self.state_dict.items():
            name = k.replace("module.", "")  # remove `module.`
            MORAN_state_dict_rename[name] = v
        self.recognizer.load_state_dict(MORAN_state_dict_rename)

        for p in self.recognizer.parameters():
            p.requires_grad = False
        self.recognizer.eval()


    def recognize(self, image):

        converter = utils.strLabelConverterForAttention(self.alphabet, ':')
        transformer = dataset.resizeNormalize((100, 32))
        image = Image.fromarray(image).convert('L')
        image = transformer(image)

        if self.cuda_flag:
            image = image.cuda()

        image = image.view(1, *image.size())
        image = Variable(image)
        text = torch.LongTensor(1 * 5)
        length = torch.IntTensor(1)
        text = Variable(text)
        length = Variable(length)

        max_iter = 20
        t, l = converter.encode('0' * max_iter)
        utils.loadData(text, t)
        utils.loadData(length, l)
        output = self.recognizer(image, length, text, text, test=True, debug=True)

        preds, preds_reverse = output[0]

        _, preds = preds.max(1)
        _, preds_reverse = preds_reverse.max(1)

        sim_preds = converter.decode(preds.data, length.data)
        sim_preds = sim_preds.strip().split('$')[0]

        return sim_preds
