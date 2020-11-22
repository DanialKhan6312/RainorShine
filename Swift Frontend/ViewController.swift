//
//  ViewController.swift
//  weatherBuddy
//
//  Created by Salvatore Giugno on 2020-11-20.
//  Copyright © 2020 Salvatore Giugno. All rights reserved.
//

import UIKit
import Foundation
import Alamofire



class ViewController: UIViewController, UIImagePickerControllerDelegate & UINavigationControllerDelegate {

    //MARK: Color!
    @IBOutlet weak var backgroundGradientView: UIView!
    
    
    //MARK: properties
    
    @IBOutlet weak var recomm: UILabel!
    
    
    
    //MARK: Actions
    @IBAction func Perfect(_ sender: UIButton) {
        
    }
    
    @IBAction func TooCold(_ sender: UIButton) {
    }
    
    @IBAction func TooHot(_ sender: UIButton) {
    }
    
    @IBAction func Wet(_ sender: UIButton) {
    }
    
    @IBAction func UploadPhoto(_ sender: UIButton) {
        
    }
    
    
    //MARK: Photo Upload

    

    //MARK: Get photo

    

    
    
    //MARK: Did Load Function
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        getit()

        

        // Create a gradient layer.
        let gradientLayer = CAGradientLayer()
        // Set the size of the layer to be equal to size of the display.
        gradientLayer.frame = view.bounds
        // Set an array of Core Graphics colors (.cgColor) to create the gradient.
        // This example uses a Color Literal and a UIColor from RGB values.
        gradientLayer.colors = [#colorLiteral(red: 0.2588235438, green: 0.7568627596, blue: 0.9686274529, alpha: 1).cgColor, UIColor(red: 0/255, green: 300/255, blue: 600/255, alpha: 0.1).cgColor]
        // Rasterize this static layer to improve app performance.
        gradientLayer.shouldRasterize = true
        // Apply the gradient to the backgroundGradientView.
        backgroundGradientView.layer.addSublayer(gradientLayer)
        
        // Diagonal: top left to bottom corner.
        gradientLayer.startPoint = CGPoint(x: 0, y: 0) // Top left corner.
        gradientLayer.endPoint = CGPoint(x: 1, y: 1) // Bottom right corner.
    }

 
    func getit(){
    let url = URL(string: "https://4b0fb3c5515f.ngrok.io/weather")!

    let task = URLSession.shared.dataTask(with: url) {(data, response, error) in
        guard let data = data else { return }
        print(String(data: data, encoding: .utf8)!)
        var stringy = String(data: data, encoding: .utf8)!
        self.recomm.text = stringy
        }
        task.resume()
    }
    
}


@IBDesignable extension UIButton {

    @IBInspectable var borderWidth: CGFloat {
        set {
            layer.borderWidth = newValue
        }
        get {
            return layer.borderWidth
        }
    }

    @IBInspectable var cornerRadius: CGFloat {
        set {
            layer.cornerRadius = newValue
        }
        get {
            return layer.cornerRadius
        }
    }

    @IBInspectable var borderColor: UIColor? {
        set {
            guard let uiColor = newValue else { return }
            layer.borderColor = uiColor.cgColor
        }
        get {
            guard let color = layer.borderColor else { return nil }
            return UIColor(cgColor: color)
        }
    }
}

struct recommend: Decodable {
let warm: Int
let wet: Int
let tempclothes: String
let rainclothes: String
    
    enum CodingKeys: String, CodingKey {
      case warm = "warm"
      case wet = "wet"
      case tempclothes = "tempclothes"
      case rainclothes = "rainclothes"

    }
}

extension ViewController {
  func fetchFilms(){
    // 1
    let request = AF.request("https://4b0fb3c5515f.ngrok.io/weather")
    // 2
    request.responseDecodable(of: recommend.self) { (response) in
      guard let rec = response.value else { return }
      print(rec.tempclothes)
        print(rec)
        print(response)
        
    }
    }
  }


extension String {
    var htmlToAttributedString: NSAttributedString? {
        guard let data = data(using: .utf8) else { return nil }
        do {
            return try NSAttributedString(data: data, options: [.documentType: NSAttributedString.DocumentType.html, .characterEncoding:String.Encoding.utf8.rawValue], documentAttributes: nil)
        } catch {
            return nil
        }
    }
    var htmlToString: String {
        return htmlToAttributedString?.string ?? ""
    }
}
